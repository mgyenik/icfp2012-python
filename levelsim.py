moves = dict({
    "left" :(-1, 0),
    "right":(1, 0),
    "down" :(0, -1),
    "up"   :(0, 1),
    "none" :(0, 0)
    })


def get_adjacent_coords(coord):
    x, y = coord
    return [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y-1)]

class MapOccupier(object):

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
            minemap.metadata["liftisopen"] = True


class Lambda(MapOccupier):
    pass


class Beard(MapOccupier):
    @staticmethod
    def tick(minemap, coord):
        if minemap.metadata.get("G") == 0:
            for c in get_adjacent_coords(coord):
                if minemap.get(c) == Air:
                    minemap[c] = Beard


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
    def tick(minemap, coord, move=None):
        Robot.actions[move](minemap, coord)
