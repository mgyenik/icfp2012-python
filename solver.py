import levelsim

def solve(root_map):
    return breadth_first(root_map)

def breadth_first(root_map):
    # Fucking robot movement is still broken
    mutable_map = root_map.clone()
    queue = [(0, mutable_map)]
    moves = 'DRUWL'
    width, height = mutable_map.metadata['dims']
    max_moves = width*height
    last_len = 0
    steps = 0
    while queue:
        steps += 1
        dist, mp = queue.pop(0)
        if last_len < len(mp.metadata['moves']):
            last_len = len(mp.metadata['moves'])
            print "length:", last_len, steps
        if mp.metadata['score'] > 0 or len(mp.metadata['moves']) >= max_moves:
            return mp.metadata['moves']
        for mv in moves:
            new_mp = mp.clone()
            new_mp.run_robot(mv)
            new_mp.tick()
            if new_mp.metadata['alive']:
                new_dist = (len(new_mp.metadata['moves'])*20 -
                            (new_mp.metadata['lambdas'] -
                             new_mp.metadata['lambdas_remaining'])*5)
                new_mp = new_mp.get_next_map()
                for i, (d, m) in enumerate(queue):
                    if d > new_dist:
                        queue.insert(i, (new_dist, new_mp))
                        break
                else:
                    queue.append((new_dist, new_mp))
