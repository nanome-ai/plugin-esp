import nanome
from nanome.api.structure import Complex
from nanome.util import Logs, Process
from nanome.util.enums import NotificationTypes
from os import path
import tempfile
import math
from .esp_config import apbs_config, pdb2pqr_config
from . import opendx_parser
from .pqr_parser import PQRStructure


class ESPProcess():

    def __init__(self, plugin: nanome.AsyncPluginInstance):
        self.__plugin = plugin

    async def run(self, src_complex: Complex):
        with tempfile.TemporaryDirectory() as work_dir:
            pdb_path = path.join(work_dir, "mol.pdb")
            pqr_path = path.join(work_dir, "mol.pqr")
            map_path = path.join(work_dir, "map")
            src_complex.io.to_pdb(pdb_path)
            try:
                await self.run_pdb2pqr(pdb_path, pqr_path)
                volume = await self.run_apbs(work_dir, pqr_path, map_path)
                # Create new copy of the Complex to avoid modifying the original
                comp = Complex.io.from_pdb(path=pdb_path)
                self._remove_ligands(comp)
                return [comp, volume]
            except Exception as e:
                Logs.error(e)
                return None

    async def run_pdb2pqr(self, pdb_path, pqr_path):
        exe_path = pdb2pqr_config["path"]
        args = pdb2pqr_config["args"] + [pdb_path, pqr_path]
        proc = Process(exe_path, args, buffer_lines=False)
        proc.on_error = Logs.warning
        proc.on_output = Logs.debug
        try:
            await proc.start()
        except Exception as e:
            self.__plugin.send_notification(NotificationTypes.error, "plugin ran into an error")
            raise e

    async def run_apbs(self, work_dir, pqr_path, map_path):
        pqr_struct = PQRStructure(pqr_path)
        box_dimensions = pqr_struct.box_dimensions

        # Fine grid lengths (fglen): [xlen][ylen][zlen]
        # dimensions in angstroms of the fine grid along the molecule X, Y, and Z axes;
        # the fine grid should enclose the region of interest in the molecule
        fglen = [x + 20.0 for x in box_dimensions]

        # Coarse grid lengths (cglen): [xlen][ylen][zlen]
        # dimensions in angstroms of the coarse grid along the molecule X, Y, and Z axes;
        # the coarse grid should completely enclose the biomolecule
        cglen = [max(x for x in fglen) + 20.0] * 3

        # Grid dimensions (dime): [nx][ny][nz]
        # grid points per processor;
        # dimensions in integer grid units along the molecule X, Y, and Z axes;
        # commonly used values are 65, 97, 129, and 161
        dime = [math.ceil(x * 2) for x in fglen]

        # Insert calculated values into config template
        apbs_in = apbs_config["template"].format(
            pqr_path, fglen[0], fglen[1], fglen[2], cglen[0], cglen[1],
            cglen[2], dime[0], dime[1], dime[2], map_path)

        exe_path = apbs_config["path"]
        with open(path.join(work_dir, "apbs.in"), "w+") as file:
            file.write(apbs_in)

        args = [path.join(work_dir, "apbs.in")]
        p = Process(exe_path, args, True)
        p.on_error = Logs.warning
        p.on_output = Logs.debug

        try:
            await p.start()
            return opendx_parser.load_file(map_path + ".dx")
        except Exception as e:
            self.__plugin.send_notification(NotificationTypes.error, "plugin ran into an error")
            raise e
    
    @staticmethod
    def _remove_ligands(comp):
        """Remove ligands from complex linked to ESP surface.
        
        The user wants to see the surface of the protein, not the ligand.
        """
        for chain in comp.chains:
            for residue in chain.residues:
                if any([atom.is_het for atom in residue.atoms]):
                    chain.remove_residue(residue)

