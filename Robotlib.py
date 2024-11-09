from canmotorlib import *
import threading
import keyboard
import can
from canheaderdict import *
import art




class Robot():
    def __init__(self,legs,motors) -> None:


        self.legs = legs
        self.motors = motors

        self.FL_leg = self.legs[0]
        self.FR_leg = self.legs[1]
        self.BL_leg = self.legs[2]
        self.BR_leg = self.legs[3]

        self.PDB_ID = 0X02



    def report_positions(self):
        def listen_for_exit():
            global running
            print("Press 'q' to stop the thread.")
            keyboard.wait('q')  # Wait until 'q' is pressed


            #TODO: fails in linux unless in root
            running = True

        threading.Thread(target=listen_for_exit,daemon=False)

        monitor_threads=[]

        for motor in self.motors:


            # thread = threading.Thread(target=motor.read_motor),daemon = True
            #threads exit when only daemon threads are left
            monitor_threads.append(threading.Thread(target=motor.read_motor,daemon = False).start())

    
    def ARM(self):

        for motor in self.motors:
            motor.ARM()

        print(art.text2art("ARMED", font='Slant'))

    def DISARM(self):

        for motor in self.motors:
            motor.DISARM()

    def KILL(self):

        for motor in self.motors:
            try:
                motor.KILL()
            except:
                print(f"no response from {motor.ID}")


    def soft_start(self):
        # Send CAN message to trigger soft start on motors packed with zeros
        ID=self.PDB_ID
        
        message = [0b010, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        self.send_can(ID,'can0',message)
        
        # self.receive_can()



    def send_can(self,ID,bus,message):
        """Sends a single message."""

        with can.Bus(interface='socketcan', channel='can0', bitrate=1000000) as bus:

            msg = can.Message(arbitration_id=ID, data=message, is_extended_id=False)

            try:
                bus.send(msg)
                print(f"Message sent on {bus.channel_info}")
            except can.CanError:
                print(f"Message NOT sent{can.CanError}")


    def receive_can(self, can_filters=None,channel='can0', bustype='socketcan', timeout=None):
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

                return message
                # print(f"Received CAN message: {message}")
                # print(f"ID: {hex(message.arbitration_id)}, Data: {message.data}, DLC: {message.dlc}")

        
        except can.CanError as e:
            print(f"CAN Error: {e}")
        except KeyboardInterrupt:
            print("Reception stopped by user.")

    def get_bat_voltage(self):
        filters = [
        {"can_id": 0x002, "can_mask": 0x7FF},  # Match exactly ID 0x002
        {"can_id": 0x001, "can_mask": 0x7FF},  
        ]

        
        message = self.receive_can(can_filters=filters)



        if message.data[0] == CAN_receive_header["CAN_MSG_BATTERY"]:
            print("wahoo")

            self.battery_voltage = message.data[1]+message.data[2]/100
            #print(f"Battery: {self.battery_voltage} v")

            return self.battery_voltage
        
        else :
            return "ERROR: No CAN Message Received"


class Leg():
    def __init__(self,shoulder_motor,knee_motor) -> None:


        self.shoulder_motor = shoulder_motor
        
        self.knee_motor = knee_motor
        print("legification initilized")


    def ARM(self):

        self.shoulder_motor.ARM()   
        self.knee_motor.ARM()

    def DISARM(self):

        self.knee_motor.DISARM()
        self.shoulder_motor.DISARM()



    def zero_calibration(self):
        velocity = 45

        knee_motor_zero = threading.Thread(target=self.knee_motor.one_side_zero_calibration, args=(-velocity,))

        shoulder_motor_zero = threading.Thread(target=self.shoulder_motor.one_side_zero_calibration, args=(velocity,))

        knee_motor_zero.start()

        shoulder_motor_zero.start()


        knee_motor_zero.join()

        shoulder_motor_zero.join()

        # self.knee_motor.one_side_zero_calibration(velocity)

        # self.shoulder_motor.one_side_zero_calibration(-velocity)


        
        





class Motor:
    def __init__(self,ID: int ,bus:str ,flip=1,motor_type="GIM8108") -> None:

        self.M = CanMotorController(bus,ID,motor_type)
        self.ID=ID
        self.posdeg=0



        #Safety
        self.posdeg_low_lim = -360
        self.posdeg_high_lim = 360


        self.kp_E_Stop = 1
        self.kd_E_Stop = 1

        
        self.cur_lim_high = 2 #amps safety stop

        self.cur_lim_low = .7 # lim for zeroing procedure

        self.flip = flip




    def ARM(self):
        #self.M.disable_motor()

        # self.E_STOP
        # pos, vel, curr = 
        self.M.enable_motor()
        

    def DISARM(self):

        self.E_STOP
        # pos_rad,vel_rad,self.current = self.M.disable_motor()
        self.M.disable_motor()
        # self.posdeg = math.degrees(pos_rad)
        # self.veldeg = math.degrees(vel_rad)


    def KILL(self):
        self.M.disable_motor()


        
    def read_motor(self):
        global running
        running=True
        

        self.ARM()


        print("__________STARTING LOG__________")
        pos=0
        kp=0
        kd=0

        while running:
            # can_id, can_dlc, data = M1._recv_can_frame()
            # positionRawValue, velocityRawValue, currentRawValue = M1.decode_motor_status(data)
            # posdeg,veldeg,curr = M1.convert_raw_to_physical_rad( positionRawValue, velocityRawValue, currentRawValue)
            
            self.posdeg,self.veldeg,self.current = self.M.send_deg_command(pos, 0, kp, kd, 0)

            print(f"ID:{self.M.motor_id} Position: {self.posdeg} rads Velocity: {self.veldeg} rad/s Current: {self.current} amps")
            time.sleep(0.5)


        # M.disable_motor()



    def safe_move(self,pos,vel,kp,kd,torque):
        # degrees
        # safe move checks for over current limit and over limit
        
        #self.prev_pos = self.posdeg
        
        #clip position to lie within range
        pos= min(max(self.posdeg_low_lim, pos), self.posdeg_high_lim)

        #move command
        #uses flip to set what side of the robot it is on
        #forward should always be positive backwards should be negtive
        #      _______
        #   (o)=======(o)    --> +
        #    \\        \\
        #    |/        |/ 
        #    @         @  

        self.posdeg,self.veldeg,self.current = self.M.send_deg_command(pos*self.flip, vel*self.flip, kp, kd, torque*self.flip)
        # delta = np.abs(self.prev_pos-self.posdeg)
        
        #Check for over current
        if self.current > self.cur_lim_high: 
            self.E_STOP()
            

    def E_STOP(self):
        #stop motor at whatever position it is curently at with estop kp kd gains

        self.posdeg,self.veldeg,self.current = self.M.send_deg_command(self.posdeg, 0, self.kp_E_Stop, self.kd_E_Stop, 0)

        print(f"Current Limit Breached: \n Motor: {self.M.motor_id} Current: {self.current} Current Limit Low:{self.cur_lim_low } Current Limit High:{self.cur_lim_high }")

        return self.posdeg,self.veldeg,self.current
    

    
    def set_zero_position(self):
        self.M.set_zero_position()
        self.posdeg=0
    

    def one_side_zero_calibration(self,velocity,timeout=1000):
        
        lim_met = False

        for _ in range(timeout):
            # self.posdeg,self.veldeg,self.current = self.M.send_deg_command(0, 40, 0, self.kd_E_Stop, 0)
            self.safe_move(0, velocity, 0, self.kd_E_Stop, 0)
            
            if np.abs(self.current) > self.cur_lim_low:
                
                self.E_STOP()
                lim_met = True
                print("Limit hit")

                break

            time.sleep(0.01)
 
        
        if lim_met == False:
            self.E_STOP()
            print("Zeroing Failed: Did not find limit")
            exit()

        return self.posdeg,lim_met


    def zero_calibration_XX(self):

        print("STARTING ZEROING")

        lim_met=False
        #enable motor
        
        self.DISARM()
        self.set_zero_position()
        self.ARM()

        

        for _ in range(1000):
            # self.posdeg,self.veldeg,self.current = self.M.send_deg_command(0, 40, 0, self.kd_E_Stop, 0)
            self.safe_move(0, -45, 0, self.kd_E_Stop, 0)
            
            if np.abs(self.current) > self.cur_lim_low:
                
                self.E_STOP()
                lim_met = True
                print("Limit hit")

                break

            time.sleep(0.01)
 
        
        if lim_met == False:
            self.E_STOP()
            print("Zeroing Failed: Did not find limit")
            exit()
    
        self.L_lim = self.posdeg


        # self.DISARM()
        # self.set_zero_position()
        # self.ARM()
        

        for _ in range(1000):

            # self.posdeg,self.veldeg,self.current = self.M.send_deg_command(0, 40, 0, self.kd_E_Stop, 0)

            self.safe_move(0, 45, 0, self.kd_E_Stop, 0)
            
            
            if np.abs(self.current) > self.cur_lim_low:
                
                self.E_STOP()
                lim_met = True

                
                break

            time.sleep(0.01)

        if lim_met == False:
            self.E_STOP()
            print("Zeroing Failed: Did not find limit")
            exit()


        
        self.R_lim = self.posdeg
        print("MOVING TO ZERO")
        time.sleep(2)


        self.safe_move((self.L_lim-self.R_lim)/2, 0, self.kp_E_Stop, self.kd_E_Stop, 0)
        time.sleep(2)


        self.DISARM()
        self.set_zero_position()
        print("ZEROING COMPLETE")


    def zero_calibration(self):
        velocity=45
        _,lim_met=self.one_side_zero_calibration(velocity)

        if lim_met == False:
            exit()

        time.sleep(2)
        # Disarm cycle sets zero?
        self.DISARM()
        self.ARM()
        self.safe_move(0,0,self.kp_E_Stop,self.kd_E_Stop,0)


        


    def crash_find_lim(self):

        print("STARTING ZEROING")

        lim_met=False
        #enable motor
        
        # self.DISARM()
        # self.set_zero_position()
        # self.ARM()

        velocity=45

    
        self.L_lim,lim_met = self.one_side_zero_calibration(velocity)

        if lim_met == False:
            exit()

        self.R_lim,lim_met = self.one_side_zero_calibration(-velocity)

        if lim_met == False:
            exit()


        np.abs(self.L_lim)-np.abs(self.R_lim)


    
        print("MOVING TO ZERO")
        time.sleep(2)


        self.safe_move((self.L_lim-self.R_lim)/2, 0, self.kp_E_Stop, self.kd_E_Stop, 0)
        time.sleep(2)


        self.DISARM()
        # self.set_zero_position()
        print("ZEROING COMPLETE")



if __name__ == "__main__":
    legs=[]
    motors_L=[]

    IDs=[10,11,12,13,14,15,16,17]
    bus=["can0","can0","can0","can0",'can1','can1','can1','can1']
    flips=[-1,-1,1,1,1,1,-1,-1,]







    for i in range(len(IDs)):
        motors_L.append(Motor(IDs[i],bus[i],flips[i],"GIM8108"))

    print(bus[0])
    for i in range(4):
        
        legs.append(Leg(motors_L[i*2],motors_L[i*2+1]))


    Bruce = Robot(legs,motors_L)

    n=5


    # M13=Motor(13,bus,1)


    # ML[0].ARM()
    # ML[0].DISARM()

    # M13.ARM()
    # M13.DISARM()

    #print(Bruce.legs[n])

    

    Bruce.soft_start()

    # print(Bruce.get_bat_voltage())
    #print(Bruce.motors[n].ID)

    print()
    Bruce.ARM()


    t=.25
    for i in range(4):

        for m in Bruce.motors:
            m.safe_move(15,0,15,1,0)

        time.sleep(t)

        for m in Bruce.motors:
            m.safe_move(0,0,15,1,0)

        time.sleep(t)

    # time.sleep(1)

    # Bruce.motors[n].one_side_zero_calibration(45)
    # for leg in Bruce.legs:
    #     leg.zero_calibration()

    # threads=[]
    # # Start a thread for each leg's zero_calibration simultaneously
    # for leg in Bruce.legs:
    #     thread = threading.Thread(target=leg.zero_calibration)
    #     thread.start()
    #     threads.append(thread)

    # # Wait for all threads to finish
    # for thread in threads:
    #     thread.join()
    
    print("threads finished")

    Bruce.DISARM()

    

    # Bruce.motors[n].zero_calibration()

    # time.sleep(2)
    # Bruce.motors[n].DISARM()
    # Bruce.DISARM()




    # Bruce.motors[n].crash_find_lim()

    # Bruce.legs[0].zero_calibration()

    # Bruce.motors[n].zero_calibration()

