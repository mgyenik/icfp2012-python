import levelsim
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
    if not 'Trampolines' in first_map.metadata:
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
    map_input = True
    map_grid = []
    line = sys.stdin.readline()
    max_len = 0
    while line:
        line = line.strip()
        if map_input and line:
            if len(line) > max_len:
                max_len = len(line)
            map_grid.append(list(line))
        else:
            if line:
                line = line.split()
                map_funcs[line[0]](line[1:]*)
        line = sys.stdin.readline()

    first_map = levelsim.Minemap()
    first_map.metadata['dims'] = (max_len, len(map_grid))
    for row, cells in enumerate(map_grid):
        if len(cells) < max_len:
            cells.append([levelsim.Air]*(max_len-len(cells)))
        for col, c in enumerate(cells):
            if c in 'ABCDEFGHI123456789':
                if not 't_coords' in map_info:
                    map_info['t_coords'] = {}
                map_info['t_coords'][c] = (row, col)
            first_map[(row, col)] = levelsim.tile_map[c]

    if 'Trampolines' in map_info:
        first_map.metadata['Trampolines'] = {}
        first_map.metadata['Targets'] = {}
        for tramp, target in map_info.iteritems():
            tramp_coord = map_info['t_coords'][tramp]
            target_coord = map_info['t_coords'][target]
            first_map.metadata['Trampolines'][tramp_coord] = target_coord
            if not target_coord in first_map.metadata['Targets']:
                first_map.metadata['Targets'][target_coord] = []
            first_map.metadata['Targets'][target_coord].append(tramp_coord)
        del map_info['Trampolines']
        del map_info['Targets']
        first_map.metadata.update(map_info)

    print first_map
