moves = {
    "left" :(-1, 0),
    "right":(1, 0),
    "down" :(0, -1),
    "up"   :(0, 1),
    "none" :(0, 0)
    }


def get_adjacent_coords(coord):
    x, y = coord
    return [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y-1)]

class MapOccupier(object):

    @classmethod
    def get_char(cls):
        raise NotImplementedError("'%s' does not yet provide get_char" % cls)

    @classmethod
    def tick(cls, minemap, coord):
        minemap[coord] = cls


class Minemap(dict):
    def __init__(self, metadata=dict()):
        #Things like Growth and Water
        self.metadata = metadata
        self.next_map = None

    def __setitem__(self, key, value):
        if value == Robot:
            self.metadata['robot_coord'] = key
        super(Minemap, self.next_map).__setitem__(key, value)

    def __str__(self):
#        for row in xrange(self.metadata['dims'][0]):
#            print ':',
#            for col in xrange(self.metadata['dims'][1]):
#                print self [(row, col)],
        result = ''
        result += super(Minemap, self).__str__()

        from pprint import pformat
        result += '\n'+pformat(self.metadata)
        return result

    def set_metadata(self, key, value):
        self.metadata[key] = value

    def get_next_map(self):
        next_map = self.next_map.clone()
        next_map.next_map = Minemap()
        return self.next_map

    def run_robot(self, move):
        Robot.tick(self, self.metadata['robot_coord'], move)

    def clone(self):
        my_clone = Minemap(metadata.copy())
        my_clone.update(self.copy())
        return myclone

    def tick(self):
        #call update on all tiles
        #write update stuff to new map and return it
        return next_map


class Earth(MapOccupier):
    pass


class Air(MapOccupier):
    pass


class LambdaLift(MapOccupier):
    @staticmethod
    def tick(minemap, coord):
        if minemap.metadata.get("lambdas_remaining") == 0:
            minemap.metadata["lift_is_open"] = True


class Razor(MapOccupier):
    pass


class Trampoline(MapOccupier):
    pass


class Target(MapOccupier):
    pass


class Beard(MapOccupier):
    @staticmethod
    def tick(minemap, coord):
        if minemap.metadata.get("G") == 0:
            for c in get_adjacent_coords(coord):
                if minemap.get(c) == Air:
                    minemap[c] = Beard


class Lambda(MapOccupier):
    pass


class Wall(MapOccupier):
    pass


class Rock(MapOccupier):
    @staticmethod
    def tick(minemap, coord):
        x, y = coord
        lower = minemap.get((x, y-1))
        if lower == Air:
            minemap[coord] = Air
            minemap[(x, y-1)] = Rock
        if lower == Rock:
            if minemap.get((x+1, y)) == Air and minemap.get((x+1, y-1)) == Air:
                minemap[coord] = Air
                minemap[(x+1, y-1)] = Rock
            elif minemap.get((x-1, y)) == Air and minemap.get((x-1, y-1)) == Air:
                 minemap[coord] = Air
                 minemap[(x-1, y-1)] = Rock
        if lower == Lambda:
            if minemap.get((x+1, y)) == Air and minemap.get((x+1, y-1)) == Air:
                minemap[coord] = Air
                minemap[(x+1, y-1)] = Rock

class Robot(MapOccupier):
    @staticmethod
    def wait(minemap, coord):
        pass

    @staticmethod
    def moveup(minemap, coord):
        movev(minemap, coord, "up")

    @staticmethod
    def movedown(minemap, coord):
        movev(minemap, coord, "down")

    @staticmethod
    def moveleft(minemap, coord):
        moveh(minemap, coord, "left")

    @staticmethod
    def moveright(minemap, coord):
        moveh(minemap, coord, "right")

    @staticmethod
    def tick(minemap, coord, move=None):
        robot_actions[move](minemap, coord)

    @staticmethod
    def shave(minemap, coord):
        razors = minemap.metadata.get("Razors")
        if razors > 0:
            minemap.metadata["Razors"] = razors-1
            for c in get_adjacent_coords:
                if minemap.get(c) == Beard:
                    minemap[c] = Air

    @staticmethod
    def moveh(minemap, coord, move):
        x, y = coord
        dx, dy = moves.get(move)
        xp = x+dx
        dest = minemap.get((xp, y))
        if dest == Air or dest == Earth:
            minemap[coord] = Air
            minemap[dest] = Robot
        if dest == Rock:
            xpp = xp+dx;
            if minemap.get((xpp, y)) == Air:
                minemap[(xpp, y)] = Rock
                minemap[dest] = Robot
                minemap[coord] = Air

    @staticmethod
    def movev(minemap, coord, move):
        x, y = coord
        dx, dy = moves.get(move)
        yp = y+dy
        dest = minemap.get((x, yp))
        if dest == Air or dest == Earth:
            minemap[coord] = Air
            minemap[dest] = Robot

tile_map = {
    ' ': Air,
    '.': Earth,
    '\\': Lambda,
    'L': LambdaLift,
    'R': Robot,
    '*': Rock,
    '#': Wall,
    'W': Beard,
    '!': Razor,
    'A': Trampoline,
    'B': Trampoline,
    'C': Trampoline,
    'D': Trampoline,
    'E': Trampoline,
    'F': Trampoline,
    'G': Trampoline,
    'H': Trampoline,
    'I': Trampoline,
    '1': Target,
    '2': Target,
    '3': Target,
    '4': Target,
    '5': Target,
    '6': Target,
    '7': Target,
    '8': Target,
    '9': Target,
}

robot_actions = {
    "S":Robot.shave,
    "L":Robot.moveleft,
    "R":Robot.moveright,
    "U":Robot.moveup,
    "D":Robot.movedown,
    None:Robot.wait
}

