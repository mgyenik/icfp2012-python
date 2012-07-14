
moves = dict({
        "left" :(-1, 0),
        "right":(1, 0),
        "down" :(0, 1),
        "up"   :(0, -1),
        "none" :(0, 0)
        })

class Minemap:
    #This is the map 
    
    def __init__(self, linkmap):
        self.next_map = linkmap
        return
        #do some stuff

    def update(self):
        #write update stuff to new map and return it
        return next_map



class Rock:
    
    coords = (0, 0)

    def __init__(self, new_coords):
        coords = new_coords
        return

    def move(self, move):
        x, y = coords
        dx, dy = moves.get(move)
        coords = (x+dx, y+dy)
        return
