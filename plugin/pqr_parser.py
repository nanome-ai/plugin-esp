import re
from nanome.util import Logs, Vector3


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

        # Strip non numeric characters from the residue number
        res_number = re.sub("[^0-9]", "", tokens[-6])
        try:
            self.__res_number = int(res_number)
        except ValueError:
            default_res_number = -1
            Logs.warning(f"Invalid residue number: {res_number}, defaulting to {default_res_number}")
            self.__res_number = default_res_number
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


class PQRStructure():

    def __init__(self, path):
        self.__atoms = []
        self.read_file(path)

    @property
    def atoms(self):
        return self.__atoms

    def read_file(self, path):
        with open(path, "r") as file:
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
