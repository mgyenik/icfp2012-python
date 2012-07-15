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
    def __init__(self, metadata=None):
        #Things like Growth and Water
        if not metadata:
            metadata = dict()
        self.metadata = metadata
        self.next_map = None

    def __setitem__(self, key, value):
        if value == Robot:
            self.metadata['robot_coord'] = key
        super(Minemap, self.next_map).__setitem__(key, value)

    def __str__(self):
        import pprint

        result = ''
        for row in xrange(self.metadata['dims'][0]-1, -1, -1):
            result += '\n:'
            for col in xrange(self.metadata['dims'][1]):
                cell = self.get((col, row))
                if cell:
                    result += cell.get_char()
                else:
                    result += '?'

        result += '\n'+pprint.pformat(self.metadata)
        return result

    def set_metadata(self, key, value):
        self.metadata[key] = value

    def get_next_map(self):
        next_map = self.next_map.clone()
        next_map.next_map = Minemap(self.next_map.metadata)
        return next_map

    def run_robot(self, move):
        tmp_map = self.clone()
        tmp_map.next_map = self
        Robot.tick(tmp_map, self.metadata['robot_coord'], move)
        self.next_map.metadata['robot_coord'] = tmp_map.metadata['robot_coord']

    def clone(self):
        my_clone = Minemap(self.metadata.copy())
        my_clone.update(self.copy())
        return my_clone

    def tick(self):
        #call update on all tiles
        for y in xrange(self.metadata['dims'][0]):
            for x in xrange(self.metadata['dims'][1]):
                self[(x, y)].tick(self, (x, y))


class Earth(MapOccupier):
    @staticmethod
    def get_char():
        return '.'


class Air(MapOccupier):
    @staticmethod
    def get_char():
        return ' '

class LambdaLift(MapOccupier):
    @staticmethod
    def tick(minemap, coord):
        if minemap.metadata.get("lambdas_remaining") == 0:
            minemap.metadata["lift_is_open"] = True
        else:
            minemap[coord] = LambdaLift

    @staticmethod
    def get_char():
        return 'L'


class Razor(MapOccupier):
    @staticmethod
    def get_char():
        return '!'


class Trampoline(MapOccupier):
    @staticmethod
    def get_char():
        return 'A'


class Target(MapOccupier):
    @staticmethod
    def get_char():
        return '1'


class Beard(MapOccupier):
    @staticmethod
    def tick(minemap, coord):
        if minemap.metadata.get("G") == 0:
            for c in get_adjacent_coords(coord):
                if minemap.get(c) == Air:
                    minemap[c] = Beard
        else:
            minemap[coord] = Beard

    @staticmethod
    def get_char():
        return 'W'


class Lambda(MapOccupier):
    @staticmethod
    def get_char():
        return '\\'


class Wall(MapOccupier):
    @staticmethod
    def get_char():
        return '#'


class Rock(MapOccupier):
    @staticmethod
    def get_char():
        return '*'

    @staticmethod
    def tick(minemap, coord):
        x, y = coord
        lower = minemap.get((x, y-1))
        if lower == Air:
            minemap[coord] = Air
            minemap[(x, y-1)] = Rock
        elif lower == Rock:
            if minemap.get((x+1, y)) == Air and minemap.get((x+1, y-1)) == Air:
                minemap[coord] = Air
                minemap[(x+1, y-1)] = Rock
            elif minemap.get((x-1, y)) == Air and minemap.get((x-1, y-1)) == Air:
                 minemap[coord] = Air
                 minemap[(x-1, y-1)] = Rock
            else:
                minemap[coord] = Rock
        elif lower == Lambda:
            if minemap.get((x+1, y)) == Air and minemap.get((x+1, y-1)) == Air:
                minemap[coord] = Air
                minemap[(x+1, y-1)] = Rock
            else:
                minemap[coord] = Rock
        else:
            minemap[coord] = Rock

class Robot(MapOccupier):
    @staticmethod
    def get_char():
        return 'R'

    @staticmethod
    def wait(minemap, coord):
        minemap[coord] = Robot

    @staticmethod
    def moveup(minemap, coord):
        Robot.movev(minemap, coord, "up")

    @staticmethod
    def movedown(minemap, coord):
        Robot.movev(minemap, coord, "down")

    @staticmethod
    def moveleft(minemap, coord):
        Robot.moveh(minemap, coord, "left")

    @staticmethod
    def moveright(minemap, coord):
        Robot.moveh(minemap, coord, "right")

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
        elif dest == Lambda:
            minemap.metadata["lambdas_remaining"] = minemap.metadata.get("lambdas_remaining") - 1
            minemap[(xp, y)] = Robot
            minemap[coord] = Air
        elif dest == Razor:
            minemap.metadata["Razors"] = minemap.metadata.get("Razors") + 1
            minemap[(xp, y)] = Robot
            minemap[coord] = Air
        elif dest == Rock:
            xpp = xp+dx;
            if minemap.get((xpp, y)) == Air:
                minemap[(xpp, y)] = Rock
                minemap[(xp, y)] = Robot
                minemap[coord] = Air
                print "foo"
                print minemap.next_map
            else:
                minemap[coord] = Robot
        else:
            print "default case"
            minemap[coord] = Robot

    @staticmethod
    def movev(minemap, coord, move):
        x, y = coord
        dx, dy = moves.get(move)
        yp = y+dy
        dest = minemap.get((x, yp))
        if dest == Air or dest == Earth:
            minemap[coord] = Air
            minemap[(x, yp)] = Robot
        elif dest == Lambda:
            minemap.metadata["lambdas_remaining"] = minemap.metadata.get("lambdas_remaining") - 1
            minemap[(xp, y)] = Robot
            minemap[coord] = Air
        elif dest == Razor:
            minemap.metadata["Razors"] = minemap.metadata.get("Razors") + 1
            minemap[(xp, y)] = Robot
            minemap[coord] = Air
        else:
            minemap[coord] = Robot

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
    "W":Robot.wait,
    None:Robot.wait,
}

