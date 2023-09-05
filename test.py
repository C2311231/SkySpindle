import random
import math
import time

# while True:
#     # Define three points on the circle
#     x1, y1, z1 = random.randint(0, 300), random.randint(0, 300), random.randint(0, 300)
#     x2, y2, z2 = random.randint(0, 300), random.randint(0, 300), random.randint(0, 300)
#     x3, y3, z3 = random.randint(0, 300), random.randint(0, 300), random.randint(0, 300)

#     A = math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
#     B = math.sqrt((x2 - x3)**2 + (y2 - y3)**2 + (z2 - z3)**2)
#     C = math.sqrt((x3 - x1)**2 + (y3 - y1)**2 + (z3 - z1)**2)

#     #Found at https://www.physicsforums.com/threads/equation-of-a-circle-through-3-points-in-3d-space.173847/ Greek000

#     R = (A*B*C)/ math.sqrt(((2*A**2)*(B**2)+(2*B**2)*(C**2)+(2*C**2)*(A**2))-(A**4)-(B**4)-(C**4)) 
    
#     print('A', x1, y1, z1)
#     print('B', x2, y2, z2)
#     print('C', x3, y3, z3)
    
#     print("Radius of the circle:", R)
#     time.sleep(3)
    


# x1, y1, z1 = 20, 10, 10
# x2, y2, z2 = 6, 3, 1
# x3, y3, z3 = 3, 67, 1

 
# A = math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
# B = math.sqrt((x2 - x3)**2 + (y2 - y3)**2 + (z2 - z3)**2)
# C = math.sqrt((x3 - x1)**2 + (y3 - y1)**2 + (z3 - z1)**2)
# print(A, B, C)
# #Found at https://www.physicsforums.com/threads/equation-of-a-circle-through-3-points-in-3d-space.173847/ Greek000

# R = (A*B*C)/ math.sqrt(((2*A**2)*(B**2)+(2*B**2)*(C**2)+(2*C**2)*(A**2))-(A**4)-(B**4)-(C**4)) 

# print('A', x1, y1, z1)
# print('B', x2, y2, z2)
# print('C', x3, y3, z3)

# print("Radius of the circle:", R)

import re 


# Example line containing letters and digits
line = 'G0X100Y50 Z3'

# Use regular expression to find and extract substrings
commands = re.findall(r'[A-Za-z]+\d+|\d+', line)

# Print the matched substrings
print(commands)
