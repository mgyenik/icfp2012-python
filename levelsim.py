moves = dict({
    "left" :(-1, 0),
    "right":(1, 0),
    "down" :(0, -1),
    "up"   :(0, 1),
    "none" :(0, 0)
    })


class MapOccupier(object):

    def __init__(self, new_coords=(0, 0)):
        self.coords = new_coords

    def update(self):
        raise NotImplementedError("update not implemented")


class Minemap(object):
    def __init__(self, linkmap=None, metadata=dict()):
        #This is the map
        self.tiles = []
        #Things like Growth and Water
        self.metadata = metadata
        if not linkmap:
            self.next_map = Minemap(self)
        else:
            self.next_map = linkmap
        #do some stuff

    def update(self):
        #call update on all tiles
        #write update stuff to new map and return it
        return next_map


class Earth(MapOccupier):

    def move(self, move):
        x, y = coords
        dx, dy = moves.get(move)
        coords = (x+dx, y+dy)

    def update(self, minemap):
        #check around you in minemap and update accordingly
        return self


class Rock(MapOccupier):

    def move(self, move):
        x, y = coords
        dx, dy = moves.get(move)
        coords = (x+dx, y+dy)

    def update(self, minemap):
        #check around you in minemap and update accordingly
        return self


class Robot(MapOccupier):

    def update(self, minemap):
        return self
