import can
import jetsonmotormodule as mm




if __name__ == "__main__":

    CAN_ID=25
    CAN_port='can0'


    # Example usage

    mmc = mm.MotorModuleController(CAN_port)		# Connect to the controller's serial port


    mmc.enable_motor(CAN_ID)							# Enable motor with CAN ID 
    #mmc.send_can_message(CAN_ID, [0x11, 0x22, 0x33, 0x44])


    #mmc.send_command(CAN_ID, 0, 0, 0, 0,  0)
