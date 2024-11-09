#python Can Test


"""
This example shows how sending a single message works.
"""

import can

def soft_start():
    # Send CAN message to trigger soft start on motors packed with zeros
    # ID=self.PDB_ID
    ID=0X02
    message = [0b010, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    send_can(ID,'can0',message)
    
    # self.receive_can()



def send_can(ID,bus,message):
    """Sends a single message."""

    with can.Bus(interface='socketcan', channel='can0', bitrate=1000000) as bus:

        msg = can.Message(arbitration_id=ID, data=message, is_extended_id=False)

        try:
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")
        except can.CanError:
            print(f"Message NOT sent{can.CanError}")

def receive_can_messages(channel='can0', bustype='socketcan', timeout=None, can_filters=None):
    try:
        # Initialize the CAN bus with filters (if provided)
        bus = can.interface.Bus(channel=channel, bustype=bustype, can_filters=can_filters)
        print(f"Listening on channel: {channel} with filters: {can_filters}")
        
        # Listen for incoming CAN messages
        while True:
            message = bus.recv(timeout)  # Blocks until a message is received or timeout occurs
            if message is None:
                print("No message received within timeout period.")
                break
            print(f"Received CAN message: {message}")
            print(f"ID: {hex(message.arbitration_id)}, Data: {message.data}, DLC: {message.dlc}")

    except can.CanError as e:
        print(f"CAN Error: {e}")
    except KeyboardInterrupt:
        print("Reception stopped by user.")




if __name__ == "__main__":
    # You can modify the filter to target specific CAN IDs or ranges of IDs
    # Example: Accept messages with arbitration ID 0x123 or 0x200
    filters = [
        {"can_id": 0x002, "can_mask": 0x7FF},  # Match exactly ID 0x01
        {"can_id": 0x001, "can_mask": 0x7FF},  # Match exactly ID 0x200
    ]

    # soft_start()
    receive_can_messages(channel='can1', bustype='socketcan', timeout=15, can_filters=filters)





