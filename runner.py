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
        map_info['Targets'] = {}
    map_info['Trampolines'][tramp] = target
    if tramp not in map_info['Targets']:
        map_info['Targets'][tramp].append(target)

map_funcs = {
    "Water":
        lambda height: set_map_info("Water", height),
    "Flooding":
        lambda ticks: set_map_info("Flooding", ticks),
    "Waterproof":
        lambda ticks: set_map_info("Waterproof", ticks),
    "Trampoline": add_trampoline,
    "Growth":
        lambda ticks: set_map_info("Growth", ticks-1),
    "Razors":
        lambda count: set_map_info("Razors", ticks),
    }

map_input = True
map_grid = []
line = sys.stdin.readline()
while line:
    line = line.strip()
    if map_input and line:
        map_grid.append(list(line))
    else:
        if line:
            line = line.split()
            map_funcs[line[0]](line[1:]*)
    line = sys.stdin.readline()
