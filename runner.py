import levelsim
import solver
import sys

# Water 0
# Flooding 10
# Waterproof 5
# Trampoline A targets 1
# Growth 25
# Razors 1
map_info = {}
def set_map_info(key, value):
    map_info[key] = value

def add_trampoline(tramp, _, target):
    if not 'Trampolines' in current_map.metadata:
        map_info['Trampolines'] = {}
    map_info['Trampolines'][tramp] = target

map_funcs = {
    'Water':
        lambda height: set_map_info('Water', height),
    'Flooding':
        lambda ticks: set_map_info('Flooding', ticks),
    'Waterproof':
        lambda ticks: set_map_info('Waterproof', ticks),
    'Trampoline': add_trampoline,
    'Growth':
        lambda ticks: set_map_info('Growth', ticks-1),
    'Razors':
        lambda count: set_map_info('Razors', ticks),
    }

if __name__ == '__main__':
    ## Read input
    map_input = True
    map_grid = []
    line = sys.stdin.readline()
    num_cols = 0
    while line:
        line = line.strip()
        if map_input and line:
            if len(line) > num_cols:
                num_cols = len(line)
            map_grid.append(list(line))
        else:
            if line:
                line = line.split()
                map_funcs[line[0]](*(line[1:]))
        line = sys.stdin.readline()

    ## Create first map
    map_info['lambdas'] = 0
    num_rows = len(map_grid)
    current_map = levelsim.Minemap()
    current_map.next_map = levelsim.Minemap()
    current_map.metadata['dims'] = (num_cols, num_rows)
    for row, cells in enumerate(map_grid):
        # Fix coordinate system
        row = (num_rows-1)-row
        if len(cells) < num_cols:
            cells.append([levelsim.Air]*(num_cols-len(cells)))
        for col, c in enumerate(cells):
            if c in 'ABCDEFGHI123456789':
                if not 't_coords' in map_info:
                    map_info['t_coords'] = {}
                map_info['t_coords'][c] = (row, col)

            # Sometimes they won't give us appropriate metadata... we'll
            # have to keep track of what hazards this map has.
            tile = levelsim.tile_map[c]
            if tile == levelsim.Lambda:
                map_info['lambdas'] += 1

            current_map[(col, row)] = tile

    ## Associate "metadata"
    if 'Trampolines' in map_info:
        current_map.metadata['Trampolines'] = {}
        current_map.metadata['Targets'] = {}
        for tramp, target in map_info.iteritems():
            tramp_coord = map_info['t_coords'][tramp]
            target_coord = map_info['t_coords'][target]
            current_map.metadata['Trampolines'][tramp_coord] = target_coord
            if not target_coord in current_map.metadata['Targets']:
                current_map.metadata['Targets'][target_coord] = []
            current_map.metadata['Targets'][target_coord].append(tramp_coord)
        del map_info['Trampolines']
        del map_info['Targets']

    current_map.metadata.update(map_info)
    current_map.metadata['score'] = 0
    current_map.metadata['moves'] = ''
    current_map.metadata['alive'] = True
    current_map.metadata['lambdas_remaining'] = map_info['lambdas']

    ## Do the first flip to a working map since we're in an odd state
    current_map.next_map.metadata = current_map.metadata.copy()
    current_map = current_map.get_next_map()

    ## Run motherfucker run!!!

    if len(sys.argv) < 2:
        solution = solver.solve(current_map)
    else:
        solution = sys.argv[1]

    for move in solution:
        print current_map
        print 'I\'m now moving %s' % move
        current_map.run_robot(move)
        current_map.tick()
        current_map = current_map.get_next_map()

    print current_map
