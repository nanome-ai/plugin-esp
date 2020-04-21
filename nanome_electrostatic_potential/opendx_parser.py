import string
from nanome.util import Vector3
from nanome.util.enums import VolumeType
from nanome._internal._volumetric._unit_cell import _UnitCell
from nanome._internal._volumetric._volume_data import _VolumeData


def load_file(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    return parse_lines([line for line in lines if not line.startswith('#')])


def parse_lines(lines):
    descrip = lines[0].split()
    if(descrip[3] != 'gridpositions'):
        raise Exception("unsupported OpenDX format {}".format(descrip[3]))

    dim = [int(x) for x in descrip[-3:]]

    origin = [float(n) for n in lines[1].split()[1:]]
    delta = [float(line.split()[i])
             for line, i in zip(lines[2:5], range(1, 4))]

    cell = _UnitCell()
    cell._A = (dim[0] - 1) * delta[0]
    cell._B = (dim[1] - 1) * delta[1]
    cell._C = (dim[2] - 1) * delta[2]
    cell._Alpha = 90.0
    cell._Beta = 90.0
    cell._Gamma = 90.0
    cell._Origin = Vector3(origin[0], origin[1], origin[2])

    volume = _VolumeData()
    volume._width = dim[0]
    volume._height = dim[1]
    volume._depth = dim[2]
    volume._mean = 0.0
    volume._rmsd = 1.0
    volume._type = VolumeType.electrostatic
    volume._name = "map.dx"
    volume._cell = cell

    datalines = lines[7:-5]
    data = [float(x) for line in datalines for x in line.split()]

    volume._data = [data[z + (y + x * dim[1]) * dim[2]] for z in range(dim[2])
                    for y in range(dim[1]) for x in range(dim[0])]
    return volume


# load_file(r"C:\Users\yzhou\AppData\Local\Temp\tmpryy_hu5e\map.dx")
