# --- Day 11: Seating System ---
# Your plane lands with plenty of time to spare.
# The final leg of your journey is a ferry that goes
# directly to the tropical island where you can finally
# start your vacation. As you reach the waiting area to
# board the ferry, you realize you're so early, nobody
# else has even arrived yet!
#
# By modeling the process people use to choose (or abandon)
# their seat in the waiting area, you're pretty sure you can
# predict the best place to sit. You make a quick map of the
# seat layout (your puzzle input).
#
# The seat layout fits neatly on a grid. Each position is either
# floor (.), an empty seat (L), or an occupied seat (#).
# For example, the initial seat layout might look like this:
#
# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# Now, you just need to model the people who will be arriving shortly.
# Fortunately, people are entirely predictable and always follow a simple
# set of rules. All decisions are based on the number of occupied seats
# adjacent to a given seat (one of the eight positions immediately up, down,
# left, right, or diagonal from the seat). The following rules are applied
# to every seat simultaneously:
#
# If a seat is empty (L) and there are no occupied seats adjacent to it,
# the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also
# occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.
# Floor (.) never changes; seats don't move, and nobody sits on the floor.
#
# After one round of these rules, every seat in the example layout becomes occupied:
#
# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##
# After a second round, the seats with four or more occupied adjacent seats become empty again:
#
# #.LL.L#.##
# #LLLLLL.L#
# L.L.L..L..
# #LLL.LL.L#
# #.LL.LL.LL
# #.LLLL#.##
# ..L.L.....
# #LLLLLLLL#
# #.LLLLLL.L
# #.#LLLL.##
# This process continues for three more rounds:
#
# #.##.L#.##
# #L###LL.L#
# L.#.#..#..
# #L##.##.L#
# #.##.LL.LL
# #.###L#.##
# ..#.#.....
# #L######L#
# #.LL###L.L
# #.#L###.##
# #.#L.L#.##
# #LLL#LL.L#
# L.L.L..#..
# #LLL.##.L#
# #.LL.LL.LL
# #.LL#L#.##
# ..L.L.....
# #L#LLLL#L#
# #.LLLLLL.L
# #.#L#L#.##
#
# #.#L.L#.##
# #LLL#LL.L#
# L.#.L..#..
# #L##.##.L#
# #.#L.LL.LL
# #.#L#L#.##
# ..L.L.....
# #L#L##L#L#
# #.LLLLLL.L
# #.#L#L#.##
# At this point, something interesting happens: the chaos stabilizes and further applications
# of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.
#
# Simulate your seating area by applying the seating rules repeatedly until no seats change state.
# How many seats end up occupied?
def getNeighbours(row, col, hall):
    rowBorders = [-1, 0, 1]
    colBorders = [-1, 0, 1]
    neighbours = []
    for i in colBorders:
        for j in rowBorders:
            r = row + j
            c = col + i
            if not (i == 0 and j == 0) and len(hall[row]) > c >= 0 and len(hall) > r >= 0:
                neighbours.append(hall[r][c])
    return neighbours


def changeSitting(row: int, col: int, hall, limit, needVisible):
    seat = hall[row][col]
    if seat == '.':
        return '.'
    neighbours = getVisibleNeighbours(row, col, hall) if needVisible else getNeighbours(row, col, hall)
    if seat == 'L' and neighbours.count('#') == 0:
        return '#'
    if seat == '#' and neighbours.count('#') >= limit:
        return 'L'
    return seat


def changeSittingForHall(hall, limit, needVisible):
    newHall = []
    for row in range(len(hall)):
        newHall.append([])
        for col in range(len(hall[row])):
            newHall[-1].append(changeSitting(row, col, hall, limit, needVisible))
        newHall[-1] = ''.join(newHall[-1])
    return newHall


def partOne(data):
    last = data.copy()
    for row in range(len(data)):
        data[row] = data[row].replace('L', '#')
    current = data
    while current != last:
        last = current.copy()
        current = changeSittingForHall(current, 4, False)
    return ''.join(current).count('#')


# --- Part Two ---
# As soon as people start to arrive, you realize your mistake.
# People don't just care about adjacent seats - they care about the first seat
# they can see in each of those eight directions!
#
# Now, instead of considering just the eight immediately adjacent seats,
# consider the first seat in each of those eight directions.
# For example, the empty seat below would see eight occupied seats:
#
# .......#.
# ...#.....
# .#.......
# .........
# ..#L....#
# ....#....
# .........
# #........
# ...#.....
# The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:
#
# .............
# .L.L.#.#.#.#.
# .............
# The empty seat below would see no occupied seats:
#
# .##.##.
# #.#.#.#
# ##...##
# ...L...
# ##...##
# #.#.#.#
# .##.##.
# Also, people seem to be more tolerant than you expected: it now takes five or
# more visible occupied seats for an occupied seat to become empty (rather than
# four or more from the previous rules). The other rules still apply: empty seats
# that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.
#
# Given the same starting layout as above, these new rules cause the seating area to shift around as follows:
#
# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL

# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##

# #.LL.LL.L#
# #LLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLLL.L
# #.LLLLL.L#

# #.L#.##.L#
# #L#####.LL
# L.#.#..#..
# ##L#.##.##
# #.##.#L.##
# #.#####.#L
# ..#.#.....
# LLL####LL#
# #.L#####.L
# #.L####.L#

# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##LL.LL.L#
# L.LL.LL.L#
# #.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLL#.L
# #.L#LL#.L#

# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.#L.L#
# #.L####.LL
# ..#.#.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#

# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.LL.L#
# #.LLLL#.LL
# ..#.L.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#
# Again, at this point, people stop shifting around and the seating area reaches equilibrium.
# Once this occurs, you count 26 occupied seats.
#
# Given the new visibility method and the rule change for occupied seats becoming empty,
# once equilibrium is reached, how many seats end up occupied?
def getVisibleNeighbours(row, col, hall):
    rowDelta = [-1, 0, 1]
    colDelta = [-1, 0, 1]
    neighbours = []
    for r in rowDelta:
        for c in colDelta:
            if not (r == 0 and c == 0):
                y = row + r
                x = col + c
                if not (len(hall) > y >= 0) or not (len(hall[y]) > x >= 0):
                    continue
                while len(hall) > y >= 0 and len(hall[y]) > x >= 0:
                    seat = hall[y][x]
                    if seat == '#':
                        neighbours.append(seat)
                        break
                    if seat == 'L':
                        break
                    y += r
                    x += c
    return neighbours


def partTwo(data):
    last = data.copy()
    for row in range(len(data)):
        data[row] = data[row].replace('L', '#')
    current = data
    while current != last:
        last = current.copy()
        current = changeSittingForHall(current, 5, True)
    return ''.join(current).count('#')


def task(data):
    hall = data.copy()
    print(partOne(hall))
    hall = data.copy()
    print(partTwo(hall))
