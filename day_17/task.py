class OneDMatrix:
    matrix = []
    len = 0

    def __init__(self):
        pass

    def __getitem__(self, index):
        return self.matrix[index]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def makeFromValue(self, value):
        self.matrix = list(value)
        self.len = len(value)
        return self

    def makeBlankBySize(self, size: int):
        self.matrix = ['.'] * size
        self.len = size
        return self

    def getNeighbours(self, x):
        rowNeighbours = [-1, 0, 1]
        if x == 0:
            rowNeighbours.remove(-1)
        if x == self.len - 1:
            rowNeighbours.remove(1)
        neighbours = []
        for row in rowNeighbours:
            neighbours.append(self[x + row])
        return neighbours

    def expand(self):
        self.matrix = ['.'] + self.matrix + ['.']
        self.len = self.getLen()

    def getLen(self):
        return len(self.matrix)

    def print(self):
        for i in range(self.len):
            print(self[i], end=' ' if i < self.len - 1 else '\n')

    def completeCycle(self):
        self.expand()
        matrix = OneDMatrix().makeBlankBySize(self.len)
        for i in range(self.len):
            cell = self[i]
            takenNeighboursCount = self.getNeighbours(i).count('#')
            if cell == '#':
                takenNeighboursCount -= 1
                matrix[i] = '#' if takenNeighboursCount in [2, 3] else '.'
            else:
                matrix[i] = '#' if takenNeighboursCount == 3 else '.'
        self.matrix = matrix.matrix

    def countTaken(self):
        return self.matrix.count('#')


class TwoDMatrix:
    matrix = []
    len = 0

    def __init__(self):
        pass

    def __getitem__(self, y):
        return self.matrix[y]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def makeFromMatrix(self, matrix):
        self.matrix = []
        for row in matrix:
            self.matrix += [OneDMatrix().makeFromValue(row)]
        self.len = self.getLen()
        return self

    def makeBlankBySize(self, xSize: int, ySize):
        self.matrix = []
        for y in range(ySize):
            self.matrix.append(OneDMatrix().makeBlankBySize(xSize))
        self.len = self.getLen()
        return self

    def getNeighbours(self, x, y):
        rowNeighbours = [-1, 0, 1]
        if y == 0:
            rowNeighbours.remove(-1)
        if y == len(self.matrix) - 1:
            rowNeighbours.remove(1)
        neighbours = []
        for column in rowNeighbours:
            neighbours += self[y + column].getNeighbours(x)
        return neighbours

    def getLen(self):
        return len(self.matrix)

    def expand(self):
        columns = self.matrix[0].len
        self.matrix = [OneDMatrix().makeBlankBySize(columns)] + self.matrix + \
                      [OneDMatrix().makeBlankBySize(columns)]
        self.len = self.getLen()
        rows = self.len
        for y in range(rows):
            self.matrix[y].expand()

    def print(self):
        for y in range(self.len):
            print('row:', y)
            for x in range(self[0].len):
                print(self[y][x], end=' ' if x < self[0].len - 1 else '\n')

    def completeCycle(self):
        self.expand()
        matrix = TwoDMatrix().makeBlankBySize(self[0].len, self.len)
        for y in range(self.len):
            for x in range(self[0].len):
                cell = self[y][x]
                takenNeighboursCount = self.getNeighbours(x, y).count('#')
                if cell == '#':
                    takenNeighboursCount -= 1
                    matrix[y][x] = '#' if takenNeighboursCount in [2, 3] else '.'
                else:
                    matrix[y][x] = '#' if takenNeighboursCount == 3 else '.'
        self.matrix = matrix.matrix

    def countTaken(self):
        res = 0
        for row in self.matrix:
            res += row.countTaken()
        return res


class ThreeDMatrix:
    matrix: [TwoDMatrix] = []
    len = 0

    def __init__(self):
        pass

    def __getitem__(self, index):
        return self.matrix[index]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def makeBlankMatrixBySizes(self, ySize, xSize, zSize=0):
        self.matrix = []
        for z in range(zSize):
            self.matrix += [TwoDMatrix().makeBlankBySize(xSize, ySize)]
        self.len = self.getLen()
        return self

    def makeFrom2DMatrix(self, twoDMatrix: [[]]):
        self.matrix = [TwoDMatrix().makeFromMatrix(twoDMatrix)]
        self.len = self.getLen()
        return self

    def getNeighbours(self, x, y, z):
        zNeighbours = [-1, 0, 1]
        if z == 0:
            zNeighbours.remove(-1)
        if z == len(self.matrix) - 1:
            zNeighbours.remove(1)
        neighbours = []
        for neighbour in zNeighbours:
            neighbours += self[z + neighbour].getNeighbours(x, y)
        return neighbours

    def getLen(self):
        return len(self.matrix)

    def expand(self):
        columns = self.matrix[0][0].len
        rows = self.matrix[0].len
        self.matrix = [TwoDMatrix().makeBlankBySize(columns, rows)] + self.matrix + \
                      [TwoDMatrix().makeBlankBySize(columns, rows)]
        self.len = self.getLen()
        layers = self.len
        for z in range(layers):
            self.matrix[z].expand()

    def print(self):
        zSize = self.len
        ySize = self[0].len
        xSize = self[0][0].len
        for z in range(zSize):
            print('z =', z)
            for y in range(ySize):
                for x in range(xSize):
                    print(self[z][y][x], end=' ' if x < xSize - 1 else '\n')

    def completeCycle(self):
        self.expand()
        xSize = self[0][0].len
        ySize = self[0].len
        zSize = self.len
        matrix = ThreeDMatrix().makeBlankMatrixBySizes(ySize, xSize, zSize)
        for z in range(zSize):
            for y in range(ySize):
                for x in range(xSize):
                    cell = self[z][y][x]
                    takenNeighboursCount = self.getNeighbours(x, y, z).count('#')
                    if cell == '#':
                        takenNeighboursCount -= 1
                        matrix[z][y][x] = '#' if takenNeighboursCount in [2, 3] else '.'
                    else:
                        matrix[z][y][x] = '#' if takenNeighboursCount == 3 else '.'
        self.matrix = matrix.matrix

    def countTaken(self):
        res = 0
        for layer in self.matrix:
            res += layer.countTaken()
        return res

# --- Day 17: Conway Cubes ---
# As your flight slowly drifts through the sky, the Elves at the Mythical
# Information Bureau at the North Pole contact you. They'd like some help
# debugging a malfunctioning experimental energy source aboard one of their super-secret imaging satellites.
#
# The experimental energy source is based on cutting-edge technology:
# a set of Conway Cubes contained in a pocket dimension! When you hear
# it's having problems, you can't help but agree to take a look.
#
# The pocket dimension contains an infinite 3-dimensional grid.
# At every integer 3-dimensional coordinate (x,y,z), there exists a
# single cube which is either active or inactive.
#
# In the initial state of the pocket dimension, almost all cubes
# start inactive. The only exception to this is a small flat region
# of cubes (your puzzle input); the cubes in this region start in the
# specified active (#) or inactive (.) state.
#
# The energy source then proceeds to boot up by executing six cycles.
#
# Each cube only ever considers its neighbors: any of the 26 other cubes
# where any of their coordinates differ by at most 1. For example, given
# the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2,
# the cube at x=0,y=2,z=3, and so on.
#
# During a cycle, all cubes simultaneously change their state according to the following rules:
#
# If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
# Otherwise, the cube becomes inactive.
# If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
# Otherwise, the cube remains inactive.
# The engineers responsible for this experimental energy source would like you to simulate
# the pocket dimension and determine what the configuration of cubes should be at the end
# of the six-cycle boot process.
#
# For example, consider the following initial state:
#
# .#.
# ..#
# ###
# Even though the pocket dimension is 3-dimensional, this initial state represents a small
# 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)
#
# Simulating a few cycles from this initial state produces the following configurations,
# where the result of each cycle is shown layer-by-layer at each given z coordinate
# (and the frame of view follows the active cells in each cycle):
#
# Before any cycles:
#
# z=0
# .#.
# ..#
# ###
#
#
# After 1 cycle:
#
# z=-1
# #..
# ..#
# .#.
#
# z=0
# #.#
# .##
# .#.
#
# z=1
# #..
# ..#
# .#.
#
#
# After 2 cycles:
#
# z=-2
# .....
# .....
# ..#..
# .....
# .....
#
# z=-1
# ..#..
# .#..#
# ....#
# .#...
# .....
#
# z=0
# ##...
# ##...
# #....
# ....#
# .###.
#
# z=1
# ..#..
# .#..#
# ....#
# .#...
# .....
#
# z=2
# .....
# .....
# ..#..
# .....
# .....
#
#
# After 3 cycles:
#
# z=-2
# .......
# .......
# ..##...
# ..###..
# .......
# .......
# .......
#
# z=-1
# ..#....
# ...#...
# #......
# .....##
# .#...#.
# ..#.#..
# ...#...
#
# z=0
# ...#...
# .......
# #......
# .......
# .....##
# .##.#..
# ...#...
#
# z=1
# ..#....
# ...#...
# #......
# .....##
# .#...#.
# ..#.#..
# ...#...
#
# z=2
# .......
# .......
# ..##...
# ..###..
# .......
# .......
# .......
# After the full six-cycle boot process completes, 112 cubes are left in the active state.
#
# Starting with your given initial configuration, simulate six cycles. How many cubes are
# left in the active state after the sixth cycle?


def partOne(data):
    matrix = ThreeDMatrix().makeFrom2DMatrix(data)
    for i in range(6):
        matrix.completeCycle()
    return matrix.countTaken()


# --- Part Two ---
# For some reason, your simulated results don't match what the experimental
# energy source engineers expected. Apparently, the pocket dimension actually
# has four spatial dimensions, not three.
#
# The pocket dimension contains an infinite 4-dimensional grid. At every
# integer 4-dimensional coordinate (x,y,z,w), there exists a single cube
# (really, a hypercube) which is still either active or inactive.
#
# Each cube only ever considers its neighbors: any of the 80 other cubes
# where any of their coordinates differ by at most 1. For example, given
# the cube at x=1,y=2,z=3,w=4, its neighbors include the cube at x=2,y=2,z=3,w=3,
# the cube at x=0,y=2,z=3,w=4, and so on.
#
# The initial state of the pocket dimension still consists of a small flat region
# of cubes. Furthermore, the same rules for cycle updating still apply: during each
# cycle, consider the number of active neighbors of each cube.
#
# For example, consider the same initial state as in the example above. Even though
# the pocket dimension is 4-dimensional, this initial state represents a small
# 2-dimensional slice of it. (In particular, this initial state defines a
# 3x3x1x1 region of the 4-dimensional space.)
#
# Simulating a few cycles from this initial state produces the following configurations,
# where the result of each cycle is shown layer-by-layer at each given z and w coordinate:
#
# Before any cycles:
#
# z=0, w=0
# .#.
# ..#
# ###
#
#
# After 1 cycle:
#
# z=-1, w=-1
# #..
# ..#
# .#.
#
# z=0, w=-1
# #..
# ..#
# .#.
#
# z=1, w=-1
# #..
# ..#
# .#.
#
# z=-1, w=0
# #..
# ..#
# .#.
#
# z=0, w=0
# #.#
# .##
# .#.
#
# z=1, w=0
# #..
# ..#
# .#.
#
# z=-1, w=1
# #..
# ..#
# .#.
#
# z=0, w=1
# #..
# ..#
# .#.
#
# z=1, w=1
# #..
# ..#
# .#.
#
#
# After 2 cycles:
#
# z=-2, w=-2
# .....
# .....
# ..#..
# .....
# .....
#
# z=-1, w=-2
# .....
# .....
# .....
# .....
# .....
#
# z=0, w=-2
# ###..
# ##.##
# #...#
# .#..#
# .###.
#
# z=1, w=-2
# .....
# .....
# .....
# .....
# .....
#
# z=2, w=-2
# .....
# .....
# ..#..
# .....
# .....
#
# z=-2, w=-1
# .....
# .....
# .....
# .....
# .....
#
# z=-1, w=-1
# .....
# .....
# .....
# .....
# .....
#
# z=0, w=-1
# .....
# .....
# .....
# .....
# .....
#
# z=1, w=-1
# .....
# .....
# .....
# .....
# .....
#
# z=2, w=-1
# .....
# .....
# .....
# .....
# .....
#
# z=-2, w=0
# ###..
# ##.##
# #...#
# .#..#
# .###.
#
# z=-1, w=0
# .....
# .....
# .....
# .....
# .....
#
# z=0, w=0
# .....
# .....
# .....
# .....
# .....
#
# z=1, w=0
# .....
# .....
# .....
# .....
# .....
#
# z=2, w=0
# ###..
# ##.##
# #...#
# .#..#
# .###.
#
# z=-2, w=1
# .....
# .....
# .....
# .....
# .....
#
# z=-1, w=1
# .....
# .....
# .....
# .....
# .....
#
# z=0, w=1
# .....
# .....
# .....
# .....
# .....
#
# z=1, w=1
# .....
# .....
# .....
# .....
# .....
#
# z=2, w=1
# .....
# .....
# .....
# .....
# .....
#
# z=-2, w=2
# .....
# .....
# ..#..
# .....
# .....
#
# z=-1, w=2
# .....
# .....
# .....
# .....
# .....
#
# z=0, w=2
# ###..
# ##.##
# #...#
# .#..#
# .###.
#
# z=1, w=2
# .....
# .....
# .....
# .....
# .....
#
# z=2, w=2
# .....
# .....
# ..#..
# .....
# .....
# After the full six-cycle boot process completes, 848 cubes are left in the active state.
#
# Starting with your given initial configuration, simulate six cycles in a 4-dimensional
# space. How many cubes are left in the active state after the sixth cycle?
class FourDMatrix:
    matrix: [ThreeDMatrix] = []
    len = 0

    def __init__(self):
        pass

    def __getitem__(self, index):
        return self.matrix[index]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def makeBlankMatrixBySizes(self, ySize, xSize, zSize=0, wSize=0):
        self.matrix = []
        for w in range(wSize):
            self.matrix += [ThreeDMatrix().makeBlankMatrixBySizes(xSize, ySize, zSize)]
        self.len = self.getLen()
        return self

    def makeFrom2DMatrix(self, twoDMatrix: [[]]):
        self.matrix = [ThreeDMatrix().makeFrom2DMatrix(twoDMatrix)]
        self.len = self.getLen()
        return self

    def getNeighbours(self, x, y, z, w):
        wNeighbours = [-1, 0, 1]
        if w == 0:
            wNeighbours.remove(-1)
        if w == len(self.matrix) - 1:
            wNeighbours.remove(1)
        neighbours = []
        for neighbour in wNeighbours:
            neighbours += self[w + neighbour].getNeighbours(x, y, z)
        return neighbours

    def getLen(self):
        return len(self.matrix)

    def expand(self):
        columns = self[0][0][0].len
        rows = self[0][0].len
        zSize = self[0].len
        self.matrix = [ThreeDMatrix().makeBlankMatrixBySizes(columns, rows, zSize)] + self.matrix + \
                      [ThreeDMatrix().makeBlankMatrixBySizes(columns, rows, zSize)]
        self.len = self.getLen()
        layers = self.len
        for w in range(layers):
            self[w].expand()

    def print(self):
        for w in range(self.len):
            print('w =', w)
            for z in range(self[0].len):
                print('z =', z)
                for y in range(self[0][0].len):
                    for x in range(self[0][0][0].len):
                        print(self[w][z][y][x], end=' ' if x < self[0][0].len - 1 else '\n')

    def completeCycle(self):
        self.expand()
        xSize = self[0][0][0].len
        ySize = self[0][0].len
        zSize = self[0].len
        matrix = FourDMatrix().makeBlankMatrixBySizes(ySize, xSize, zSize, self.len)
        for w in range(self.len):
            for z in range(zSize):
                for y in range(ySize):
                    for x in range(xSize):
                        cell = self[w][z][y][x]
                        takenNeighboursCount = self.getNeighbours(x, y, z, w).count('#')
                        if cell == '#':
                            takenNeighboursCount -= 1
                            matrix[w][z][y][x] = '#' if takenNeighboursCount in [2, 3] else '.'
                        else:
                            matrix[w][z][y][x] = '#' if takenNeighboursCount == 3 else '.'
        self.matrix = matrix.matrix

    def countTaken(self):
        res = 0
        for layer in self.matrix:
            res += layer.countTaken()
        return res


def partTwo(data):
    matrix = FourDMatrix().makeFrom2DMatrix(data)
    for i in range(6):
        matrix.completeCycle()
    return matrix.countTaken()


def task(data):
    print(partOne(data))
    print(partTwo(data))
