import numpy as np
max = 2**16-1

zero = max/2

rotations = 2




delta_90_deg = zero/rotations/4

abs_90_deg = zero + delta_90_deg


d_angle = 360*2  *4096/675

abs_angle = zero + d_angle

print("rad limit",2**15 *675/4096/360 )

print("delta_90_deg:",delta_90_deg)
print("Hex for 00 deg:",hex(int(zero)))
print("Hex for 90 deg:",hex(int(abs_90_deg)))
print("Hex for 90 deg actually:",hex(int(abs_angle)))





raw1=32767
raw2=30582
delta = raw2-raw1



rot = delta* 15/2**15
print(rot)

