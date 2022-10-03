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
                comp = Complex.io.from_pdb(path=pdb_path)
                return [comp, volume]
            except Exception as e:
                Logs.error(e)
                return None

    async def run_pdb2pqr(self, pdb_path, pqr_path):
        exe_path = pdb2pqr_config["path"]
        args = pdb2pqr_config["args"] + [pdb_path, pqr_path]
        proc = Process(exe_path, args)
        proc.on_error = Logs.warning
        proc.on_output = Logs.debug
        try:
            await proc.start()
        except Exception as e:
            self.__plugin.send_notification(NotificationTypes.error, "plugin ran into an error")
            raise e

    async def run_apbs(self, work_dir, pqr_path, map_path):
        ext_min = [None, None, None]
        ext_max = [None, None, None]
        pqr_struct = PQRStructure(pqr_path)
        for atom in pqr_struct.atoms:
            if ext_min[0] is None or atom.position.x < ext_min[0]:
                ext_min[0] = atom.position.x
            if ext_max[0] is None or atom.position.x > ext_max[0]:
                ext_max[0] = atom.position.x
            if ext_min[1] is None or atom.position.y < ext_min[1]:
                ext_min[1] = atom.position.y
            if ext_max[1] is None or atom.position.y > ext_max[1]:
                ext_max[1] = atom.position.y
            if ext_min[2] is None or atom.position.z < ext_min[2]:
                ext_min[2] = atom.position.z
            if ext_max[2] is None or atom.position.z > ext_max[2]:
                ext_max[2] = atom.position.z

        ext = [x - y for x, y in zip(ext_max, ext_min)]

        fglen = [x + 20.0 for x in ext]
        cglen = [max(x for x in fglen) + 20.0] * 3
        dime = [math.ceil(x * 2) for x in fglen]

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
