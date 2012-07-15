moves = dict({
    "left" :(-1, 0),
    "right":(1, 0),
    "down" :(0, -1),
    "up"   :(0, 1),
    "none" :(0, 0)
    })


class MapOccupier(object):

    def tick(self):
        raise NotImplementedError("update not implemented")


class Minemap(dict):
    def __init__(self, metadata=dict()):
        #Things like Growth and Water
        self.metadata = metadata

    def __setitem__(self, key, value):
        if value == Robot:
            self.metadata['robot_coord'] = key
        super(Minemap, self.next_map).__setitem__(key, value)

    def clone(self):
        my_clone = Minemap(metadata.copy())
        my_clone.update(self.copy())
        return myclone

    def tick(self):
        #call update on all tiles
        #write update stuff to new map and return it
        return next_map


class Earth(MapOccupier):

    @staticmethod
    def tick(minemap):
        #check around you in minemap and update accordingly
        return self


class Air(MapOccupier):

    @staticmethod
    def tick(minemap):
        #I MAKE NO CHANGES
        pass


class LambdaLift(MapOccupier):
    isopen = False
    @staticmethod
    def tick():
        if Lambda.lambdas_remaining == 0:
            isopen = True


class Lambda(MapOccupier):
    lambdasremaining = 0
    @staticmethod
    def tick():
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
             else if minemap.get((x-1, y)) == Air and minemap.get((x-1, y-1)) == Air:
        if lower == Lambda:
            if minemap.get((x+1, y)) == Air and minemap.get((x+1, y-1)) == Air:
                minemap[coord] = Air
                minemap[(x+1, y-1)] = Rock

class Robot(MapOccupier):

    @staticmethod
    def tick(minemap):
        pass
