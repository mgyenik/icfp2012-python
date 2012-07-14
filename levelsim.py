
moves = dict({
        "left" :(-1, 0),
        "right":(1, 0),
        "down" :(0, 1),
        "up"   :(0, -1),
        "none" :(0, 0)
        })

class MapOccupier(object):
    def update(self):
        raise NotImplementedError("update not implemented")

class Minemap(object):
    #This is the map 
    tiles = []

    def __init__(self, linkmap):
        self.next_map = linkmap
        return
        #do some stuff

    def update(self):
        #call update on all tiles
        #write update stuff to new map and return it
        return next_map



class Rock(MapOccupier):
    
    coords = (0, 0)

    def __init__(self, new_coords):
        coords = new_coords
        return

    def move(self, move):
        x, y = coords
        dx, dy = moves.get(move)
        coords = (x+dx, y+dy)
        return

    def update(self, minemap):
        #check around you in minemap and update accordingly
        return self


class Robot(MapOccupier):
    coords = (0, 0)

    def __init__(self, new_coords):
        coords = new_coords
        return
    
    def update(self, minemap):
        return self
