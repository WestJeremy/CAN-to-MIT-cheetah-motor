'''
Ben Katz
Jeremy West
Motor Module Python API
adapted for Nvidia Jetson agx Orin

Assumes the serial device is a nucleo running the firmware at:
Corresponding STM32F446 Firmware here:
https://os.mbed.com/users/benkatz/code/CanMaster/
'''
import serial
from struct import *
import time
import can

class MotorModuleController():
    def __init__(self, CAN_port='can0'):
        try:
            self.CAN_port=CAN_port
            
            self.bus = can.interface.Bus(self.CAN_port, interface='socketcan', fd=True)
            
            self.rx_data = [0, 0, 0, 0, 0, 0]
            self.rx_values = [0, 0, 0, 0]
            self.tx_data = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            print('connected to motor module controller')
        except:
            print('failed to connect to motor module controller')
            pass
    def send_data(self):
        pass



    def send_can_message(self,arbitration_id, data=[0x01, 0x02, 0x03, 0x04]):
        """
        Send a CAN message on the specified bus.
        :param arbitration_id: The arbitration ID of the CAN message.
        :param data: The data payload of the CAN message as a list of bytes.
        """
        
        # Create a CAN message
        message = can.Message(arbitration_id=arbitration_id,
                            data=data,
                            is_fd=True,
                            is_extended_id=True)

        print("")
        print(f"Attempting to send message: {message}")
        print("")

        try:
            # Send the message on the CAN bus
            self.bus.send(message)
            print(f"Message sent on {self.CAN_port}: {message}")
        except can.CanError as e:


            print(f"Failed to send message: {e}")




    def send_command(self, id, p_des, v_des, kp, kd, i_ff):
            """
            send_command(desired position, desired velocity, position gain, velocity gain, feed-forward current)

            Sends data over CAN, reads response, and populates rx_data with the response.
            """
            id =  int(id)
            b =  pack("f", p_des) + pack("f", v_des) + pack("f", kp) + pack("f", kd) + pack("f", i_ff)
            #print(int.from_bytes(b, byteorder='big'))
            
            #bytes(bytearray([id]))
            self.send_can_message(id,b)


            #print(self.rx_values)



    def enable_motor(self, id):
        """
        Puts motor with CAN ID "id" into torque-control mode.  2nd red LED will turn on
        """
        b = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFC'
        b = b
        #id = bytes(bytearray([id]))
        id = int(id)

        try: 
            self.send_can_message(id,b)

            print('motor enabled')
        except can.CanError as e:
            

            print('failed to enable motor')
            print(f"Failed to send message: {e}")
            pass

        #time.sleep(.1)
        #self.ser.flushInput()


    def disable_motor(self, id):
        """
        Removes motor with CAN ID "id" from torque-control mode.  2nd red LED will turn off
        """
        b = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFD'
        b = b + bytes(bytearray([id]))


        id = int(id)
        self.send_can_message(id,b)
        
    def zero_motor(self, id):
        pass




if __name__ == "__main__":

    CAN_ID=25
    
    CAN_port='can0'


    # Example usage


    mmc = MotorModuleController(CAN_port)		# Connect to the controller's serial port


    mmc.enable_motor(CAN_ID)							# Enable motor with CAN ID 
    mmc.set_zero_position()
    #listener = SomeListener()

    #for msg in mmc.bus:
    #    print("")
    #    print(msg.data)
    #    print("")

    #print("No more messages")
    
    


    mmc.send_command(CAN_ID, 2, 0, 1, 1, 0)
    #mmc.send_deg_command(365, 0, 1, 1, 0)
    
    #mmc.disable_motor()

