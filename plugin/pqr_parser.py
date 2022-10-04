import re
from nanome.util import Logs, Vector3


class Atom():

    def __init__(self, tokens):
        self.__position = Vector3(tokens[-5], tokens[-4], tokens[-3])

    @property
    def position(self):
        return self.__position


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
                tokens = line.split()
                if tokens[0] == "REMARK":
                    return
                elif tokens[0] == "ATOM" or tokens[0] == "HETATOM":
                    self.atoms.append(Atom(tokens))
