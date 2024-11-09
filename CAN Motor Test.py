#CAN Motor Test 

from canmotorlib import *
import time



def test_move_deg(pos):

    input(f"MOVING TO {pos} DEGREES PRESS: PRESS ANY KEY")
    for _ in range (5):
        posdeg,veldeg,curr=M1.send_deg_command(pos, 0, 3, 1, 0)
    
    
        print("*************************************")
        print(f"Position: {posdeg} deg \n Velocity: {veldeg} deg/s \n Current: {curr} amps")
        print("*************************************")
        time.sleep(0.01)

def test_move_rad(rad_pos):

    # MOVE TO RAD POS
    input(f"MOVING TO {rad_pos} RADS PRESS: PRESS ANY KEY")
    posdeg,veldeg,curr=M1.send_rad_command(rad_pos, 0, 3, 1, 0)
    time.sleep(1.5)
    print("*************************************")
    print(f"Position: {posdeg} rads \n Velocity: {veldeg} rad/s \n Current: {curr} amps")
    print("*************************************")


def test_move_raw(raw_pos):

    # MOVE TO RAW POS
    input(f"MOVING TO {raw_pos} RAW PRESS: PRESS ANY KEY")
    posdeg,veldeg,curr=M1._send_raw_command(raw_pos, 0, 3, 1, 0)
    time.sleep(1.5)
    print("*************************************")
    print(f"Position: {posdeg} __ \n Velocity: {veldeg} __/s \n Current: {curr} amps")
    print("*************************************")

def test_move_admin(msg):
    input(f"MOVING: PRESS ANY KEY")

    M1._send_can_frame_ADMIN(msg)
    time.sleep(1.5)
    print("*************************************")



M1 = CanMotorController('can0',25,"GIM8108")
M1.enable_motor()
print("***************MOTOR ENABLED***************")

M1.set_zero_position()
print("ZERO POSIION SET")


# ___________MOVE COMMANDS___________
# MOVE TO ZERO POSITION

#   TEST POSITIONS
deg_pos = 720

rad_pos = 2*np.pi/4
raw_pos = 1


msg_pos_set_00 = b'\x19\x00\x00\x00\x08\x00\x00\x00\x7f\xff\x7f\xf0\x1837\xff'
msg_pos_set_90 = b'\x19\x00\x00\x00\x08\x00\x00\x00\x91\x10\x7f\xf0\x1837\xff'
#                                                   ^^^^^^^ positions





test_move_deg(0)
test_move_deg(deg_pos)
test_move_deg(0)



# test_move_rad(0)
# test_move_rad(rad_pos)
# test_move_rad(0)

# test_move_rad(0)
# test_move_rad(1)
# test_move_rad(0)
# test_move_admin(msg_pos_set_00)
# test_move_admin(msg_pos_set_90)
# test_move_admin(msg_pos_set_00)
# test_move_rad(0)


# test_move_raw(0)
# test_move_raw(raw_pos)
# test_move_raw(0)




time.sleep(1.5)
M1.disable_motor()
print("***************MOTOR DISABLED***************")




