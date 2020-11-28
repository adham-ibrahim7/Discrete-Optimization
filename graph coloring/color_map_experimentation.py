from collections import defaultdict

color_map = defaultdict(list)

color_map[0] += [1]
color_map[0] += [2]
color_map[1] += [1]

print(color_map)
