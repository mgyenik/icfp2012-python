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

    def tick(self, minemap):
        #check around you in minemap and update accordingly
        return self


class Rock(MapOccupier):

    def move(self, move):
        x, y = coords
        dx, dy = moves.get(move)
        coords = (x+dx, y+dy)

    def tick(self, minemap):
        #check around you in minemap and update accordingly
        return self


class Robot(MapOccupier):

    def tick(self, minemap):
        return self
