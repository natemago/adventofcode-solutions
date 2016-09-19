#!/usr/bin/python3

def paper_area_and_ribbon_needed(present_dims):
  sides_areas = [present_dims[0]*present_dims[1], present_dims[1]*present_dims[2], present_dims[0]*present_dims[2]]
  smallest_side = min(sides_areas)
  
  present_dims.sort()
  smallest_sides = present_dims[0:2]
  
  
  return (sum(sides_areas)*2 + smallest_side, sum(smallest_sides)*2 + present_dims[0]*present_dims[1]*present_dims[2])




total_area = 0
total_ribbon = 0

with open('input') as f:
  line = f.readline()
  while line:
    area,ribbon = paper_area_and_ribbon_needed([int(dim) for dim in line.split('x')])
    
    total_area += area
    total_ribbon += ribbon
    
    line = f.readline()

print(total_area)
print(total_ribbon)