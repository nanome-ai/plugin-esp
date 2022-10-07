from nanome.util import Vector3

class PQRStructure():

    def __init__(self, path):
        self.atom_positions = []
        self.read_file(path)

    def read_file(self, path):
        with open(path, "r") as file:
            lines = file.readlines()
            for line in lines:
                tokens = line.split()
                if tokens[0] == "REMARK":
                    continue
                elif tokens[0] == "ATOM" or tokens[0] == "HETATOM":
                    atom_position = Vector3(tokens[-5], tokens[-4], tokens[-3])
                    self.atom_positions.append(atom_position)

    @property
    def box_dimensions(self):
        """Dimensions of a box that encloses the entire molecule."""
        ext_min_x = min(pos.x for pos in self.atom_positions)
        ext_min_y = min(pos.y for pos in self.atom_positions)
        ext_min_z = min(pos.z for pos in self.atom_positions)
        ext_max_x = max(pos.x for pos in self.atom_positions)
        ext_max_y = max(pos.y for pos in self.atom_positions)
        ext_max_z = max(pos.z for pos in self.atom_positions)
        ext_min = [ext_min_x, ext_min_y, ext_min_z]
        ext_max = [ext_max_x, ext_max_y, ext_max_z]
        ext = [y - x for x, y in zip(ext_min, ext_max)]
        return ext
    
