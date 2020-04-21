import nanome
import string
from nanome.util import Vector3
from nanome._internal._structure import _Complex, _Molecule, _Chain, _Residue, _Atom


class Atom():
    def __init__(self, tokens):
        self.__is_het = tokens[0] != "ATOM"
        self.__atom_number = int(tokens[1])
        self.__atom_name = tokens[2]
        self.__res_name = tokens[3]
        if len(tokens) > 10:
            self.__chain_id = tokens[4]
        else:
            self.__chain_id = None
        self.__res_number = int(tokens[-6])
        self.__position = Vector3(tokens[-5], tokens[-4], tokens[-3])
        self.__charge = float(tokens[-2])
        self.__radius = float(tokens[-1])

    @property
    def is_het(self):
        return self.__is_het

    @property
    def atom_number(self):
        return self.__atom_number

    @property
    def atom_name(self):
        return self.__atom_name

    @property
    def residue_name(self):
        return self.__res_name

    @property
    def chain_id(self):
        chain = self.__chain_id
        if chain is None:
            chain = 'A'
        if self.is_het:
            return 'H' + chain
        else:
            return chain

    @property
    def residue_number(self):
        return self.__res_number

    @property
    def position(self):
        return self.__position

    @property
    def charge(self):
        return self.__charge

    @property
    def radius(self):
        return self.__radius


class Structure():
    def __init__(self, path):
        self.__atoms = []
        self.read_file(path)

    @property
    def atoms(self):
        return self.__atoms

    def read_file(self, path):
        file = open(path, "r")
        lines = file.readlines()
        for line in lines:
            self.read_line(line)

    def read_line(self, line):
        tokens = line.split()
        if tokens[0] == "REMARK":
            return
        elif tokens[0] == "ATOM" or tokens[0] == "HETATOM":
            self.read_coord(tokens)

    def read_coord(self, tokens):
        self.__atoms.append(Atom(tokens))


def structure_to_complex(structure: Structure):
    residues = {}
    chains = {}
    for pqr_atom in structure.atoms:
        atom = _Atom._create()
        atom._symbol = pqr_atom.atom_name[:1]
        atom._serial = pqr_atom.atom_number
        atom._name = pqr_atom.atom_name
        atom._position = pqr_atom.position
        atom._is_het = pqr_atom.is_het

        if not pqr_atom.chain_id in chains:
            chain = _Chain._create()
            chain._name = pqr_atom.chain_id
            chains[pqr_atom.chain_id] = chain

        if not pqr_atom.residue_number in residues:
            residue = _Residue._create()
            residue._name = pqr_atom.residue_name
            residue._type = pqr_atom.residue_name
            residue._serial = pqr_atom.residue_number
            residues[pqr_atom.residue_number] = residue
            chains[pqr_atom.chain_id]._add_residue(residue)

        residues[pqr_atom.residue_number]._add_atom(atom)

    mol = _Molecule._create()
    for chain in chains:
        mol._add_chain(chains[chain])

    complex = _Complex._create()
    complex._add_molecule(mol)
    return complex._convert_to_conformers()


def load_pqr(path):
    structure = Structure(path)
    structure_to_complex(structure)
