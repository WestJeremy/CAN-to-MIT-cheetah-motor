import struct
from bitstring import BitArray
import numpy as np

maxRawPosition = 2**16 - 1                      # 16-Bits for Raw Position Values
maxRawVelocity = 2**12 - 1                      # 12-Bits for Raw Velocity Values

def float_to_uint(x, x_min, x_max, numBits):
    span = x_max - x_min
    offset = x_min
    # Attempt to speedup by using pre-computation. Not used currently.
    if numBits == 16:
        bitRange = maxRawPosition
    elif numBits == 12:
        bitRange = maxRawVelocity
    else:
        bitRange = 2**numBits - 1
    return int(((x - offset) * (bitRange)) / span)

def _send_can_frame(data):
    """
    Send raw CAN data frame (in bytes) to the motor.
    """
    can_dlc = len(data)
    print(f"sending CAN data:{data}")
    can_msg = struct.pack(can_frame_fmt_send, motor_id, can_dlc, data)

    print(f"sending CAN message:{can_msg}")
   

motorParams = {
                "P_MIN" : -4* np.pi,
                "P_MAX" : 4* np.pi,
                "V_MIN" : -45.0,
                "V_MAX" : 45.0,
                "KP_MIN" : 0.0,
                "KP_MAX" : 500,
                "KD_MIN" : 0.0,
                "KD_MAX" : 5.0,
                "T_MIN" : -18.0,
                "T_MAX" : 18.0,
                "AXIS_DIRECTION" : -1
                }

_p_des_BitArray = BitArray(
    uint=float_to_uint(0, motorParams["P_MIN"], motorParams["P_MAX"], 16), length=16
)
_v_des_BitArray = BitArray(
    uint=float_to_uint(0, motorParams["V_MIN"], motorParams["V_MAX"], 12), length=12
)
_kp_BitArray = BitArray(uint=0, length=12)
_kd_BitArray = BitArray(uint=0, length=12)
_tau_BitArray = BitArray(uint=0, length=12)
_cmd_bytes = BitArray(uint=0, length=64)
_recv_bytes = BitArray(uint=0, length=48)

p_des_rad = 1
v_des_rad=0
kp=0
kd=0
tau_ff=0

rawPosition = float_to_uint(p_des_rad, motorParams["P_MIN"], motorParams["P_MAX"], 16)
rawVelocity = float_to_uint(v_des_rad, motorParams["V_MIN"], motorParams["V_MAX"], 12)
rawTorque = float_to_uint(tau_ff, motorParams["T_MIN"], motorParams["T_MAX"], 12)

# rawKp = (maxRawKp * kp) / motorParams["KP_MAX"]

# rawKd = (maxRawKd * kd) / motorParams["KD_MAX"]

_p_des_BitArray.uint = float_to_uint(p_des_rad, motorParams["P_MIN"], motorParams["P_MAX"], 16)
_v_des_BitArray.uint = v_des_rad
_kp_BitArray.uint = kp
_kd_BitArray.uint = kd
_tau_BitArray.uint = tau_ff

cmd_BitArray = (
    _p_des_BitArray.bin
    + _v_des_BitArray.bin
    + _kp_BitArray.bin
    + _kd_BitArray.bin
    + _tau_BitArray.bin
)

_cmd_bytes.bin = cmd_BitArray

can_frame_fmt_send="=IB3x8s"
motor_id= 25


_send_can_frame(_cmd_bytes.tobytes())