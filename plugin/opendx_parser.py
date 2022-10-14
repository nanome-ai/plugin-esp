from nanome.util import Vector3
from nanome.util.enums import VolumeType
from nanome._internal._volumetric._unit_cell import _UnitCell
from nanome._internal._volumetric._volume_data import _VolumeData

"""
Example opendx file:

# Comments
object 1 class gridpositions counts nx ny nz
origin xmin ymin zmin
delta hx 0.0 0.0
delta 0.0 hy 0.0 
delta 0.0 0.0 hz
object 2 class gridconnections counts nx ny nz
object 3 class array type double rank 0 times n
u(0,0,0) u(0,0,1) u(0,0,2)
...
u(0,0,nz-3) u(0,0,nz-2) u(0,0,nz-1)
u(0,1,0) u(0,1,1) u(0,1,2)
...
u(0,1,nz-3) u(0,1,nz-2) u(0,1,nz-1)
...
u(0,ny-3,nz-3) u(0,ny-2,nz-2) u(0,ny-1,nz-1)
u(1,0,0) u(1,0,1) u(1,0,2)
...
attribute "dep" string "positions"
object "regular positions regular connections" class field
component "positions" value 1
component "connections" value 2
component "data" value 3
"""


def load_file(path):
    with open(path, "r") as file:
        lines = file.readlines()
        non_comment_lines = [line for line in lines if not line.startswith('#')]
        return parse_lines(non_comment_lines)


def parse_lines(lines):
    description_line = lines[0].split()
    origin_line = lines[1].split()
    delta_lines = lines[2:5]
    data_lines = lines[7:-5]

    if(description_line[3] != 'gridpositions'):
        raise Exception("unsupported OpenDX format {}".format(description_line[3]))

    dim = [int(x) for x in description_line[-3:]]
    origin = [float(n) for n in origin_line[1:]]

    delta_x = float(delta_lines[0].split()[1])
    delta_y = float(delta_lines[1].split()[2])
    delta_z = float(delta_lines[2].split()[3])
    delta = [delta_x, delta_y, delta_z]

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

    data = []
    for line in data_lines:
        # Each line of data should be 3 float values
        tokens = [float(val) for val in line.split()]
        data.extend(tokens)

    volume._data = [
        data[z + (y + x * dim[1]) * dim[2]]
        for z in range(dim[2])
        for y in range(dim[1])
        for x in range(dim[0])
    ]
    return volume
