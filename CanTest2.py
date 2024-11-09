import can

def send_can_message(interface='can0', arbitration_id=0x123, data=[0x01, 0x02, 0x03, 0x04]):
    """
    Send a CAN message on the specified interface.

    :param interface: The CAN interface (e.g., 'can0').
    :param arbitration_id: The arbitration ID of the CAN message.
    :param data: The data payload of the CAN message as a list of bytes.
    """
    # Create a CAN bus object using the specified interface
    bus = can.interface.Bus(interface, interface='socketcan')

    # Create a CAN message
    message = can.Message(arbitration_id=arbitration_id,
                          data=data,
                          is_extended_id=False)

    try:
        # Send the message on the CAN bus
        bus.send(message)
        print(f"Message sent on {interface}: {message}")
    except can.CanError as e:
        print(f"Failed to send message: {e}")

if __name__ == "__main__":
    # Example usage
    send_can_message(interface='can0', arbitration_id=0x123, data=[0x11, 0x22, 0x33, 0x44])
