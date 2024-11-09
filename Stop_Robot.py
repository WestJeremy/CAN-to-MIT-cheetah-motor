from Robotlib import *


legs=[]
motors=[]

IDs=[10,11,12,13,14,15,16,17]
bus=['can0','can0','can0','can0','can1','can1','can1','can1']
flips=[-1,-1,-1,-1,1,1,1,1,]



for i in range(len(IDs)):
    motors.append(Motor(IDs[i],bus[i],flips[i]))


for i in range(4):
    
    legs.append(Leg(motors[i*2],motors[i*2+1]))


Bruce = Robot(legs,motors)

n=2
# print(Bruce.legs[n])


# Bruce.ARM()

Bruce.KILL()



