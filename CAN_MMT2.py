
import can


def send_one(message):
    """Sends a single message."""

    # this uses the default configuration (for example from the config file)
    # see https://python-can.readthedocs.io/en/stable/configuration.html
    with can.Bus('can0', interface='socketcan') as bus:
        # Using specific buses works similar:
        # bus = can.Bus(interface='socketcan', channel='vcan0', bitrate=250000)
        # bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=250000)
        # bus = can.Bus(interface='ixxat', channel=0, bitrate=250000)
        # bus = can.Bus(interface='vector', app_name='CANalyzer', channel=0, bitrate=250000)
        # ...
        
 

        msg = can.Message(
            arbitration_id=25, data=message, is_extended_id=False
        )

        try:
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")
            print("")
            print(f"Message sent: {msg}")
            print("")


        except can.CanError:
            print("Message NOT sent")


# Function to convert integer inputs to the suitable bit-length values
def convert_to_hex(value, bit_length):
    max_value = (1 << bit_length) - 1
    if value < 0 or value > max_value:
        raise ValueError(f"Value {value} is out of range for {bit_length} bits.")
    return value


if __name__ == "__main__":


    # Input integer values
    pos = int(1)
    vel = int(0)
    kp = int(1)
    kd = int(0)
    ff = int(0)

    # Convert integers to appropriate hex values
    pos = convert_to_hex(pos, 16)
    vel = convert_to_hex(vel, 12)
    kp = convert_to_hex(kp, 12)
    kd = convert_to_hex(kd, 12)
    ff = convert_to_hex(ff, 12)

    # Create an empty list to store the CAN message (8 bytes)
    can_msg = [0] * 8

    # Pack the values into the CAN message array
    can_msg[0] = (pos >> 8) & 0xFF
    can_msg[1] = pos & 0xFF
    can_msg[2] = (vel >> 4) & 0xFF
    can_msg[3] = ((vel & 0x000F) << 4) + ((kp >> 8) & 0x0F)
    can_msg[4] = kp & 0xFF
    can_msg[5] = (kd >> 4) & 0xFF
    can_msg[6] = ((kd & 0x000F) << 4) + ((ff >> 8) & 0x0F)
    can_msg[7] = ff & 0xFF



    #send_one(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFC')
    send_one(can_msg)