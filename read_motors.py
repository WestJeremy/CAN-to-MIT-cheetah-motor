import threading
import time
import csv
import random
import canmotorlib as cm
import keyboard

# Shared data structure for logging
log_data = []
lock = threading.Lock()
stop_logging = threading.Event()


# Function to be executed by the first thread
def move_motor():
    global log_data, M1, time_init,Motor_Complete


    Motor_Complete = False

    M1 = cm.CanMotorController('can0',25,"GIM8108")
    M1.enable_motor()
    M1.set_zero_position()

    print("__________STARTING STEP RESPONSE__________")

    time.sleep(1)
    time_init = time.time()
    M1.send_deg_command(365, 0, 1, 1, 0)
    time.sleep(.001)

    

    Motor_Complete = True
    print("__________MOTOR MOVEMENT COMPLETE__________")
    M1.disable_motor()
    print("Motor Step: COMPLETE")

    



# Function to be executed by the first thread
def write_to_log(dt=0.05):
    global log_data, M1, time_init

    c=0

    time.sleep(.01)
    
        

    while True:  # Simulate running the function 10 times
        with lock:
            #Get Motor data and convert it to rads
            #print(M1._recv_can_frame())
            try:
                can_id, can_dlc, motorStatusData = M1._recv_can_frame() #CAN HEX
                rawMotorData = M1.decode_motor_status(motorStatusData)  #bit mapped
                pos, vel, curr = M1.convert_raw_to_physical_rad(rawMotorData[0], rawMotorData[1], rawMotorData[2])  #in rads

                #Record data to Log
                data = pos, vel, curr  # get pos, vel, curr
                timestamp = time.time() - time_init  # Record the current timestamp
                log_data.append((timestamp, data))  # Add data to the log
                c += 1
            except:
                pass
            time.sleep(dt)  # step time
            if Motor_Complete:
                break
    # Signal that the function is done
    stop_logging.set()
    print(f"c:{c}")
    print("write to log: COMPLETE")


# Function to be executed by the first thread
def function_to_run():
    global log_data
    for _ in range(10):  # Simulate running the function 10 times
        with lock:
            # Simulating some data processing
            data = random.randint(0, 100)  # Generate a random number as sample data
            timestamp = time.time()  # Record the current timestamp
            log_data.append((timestamp, data))  # Add data to the log
        time.sleep(1)  # Simulate processing time
    # Signal that the function is done
    stop_logging.set()

# Function to be executed by the second thread
def log_to_csv(filename='log.csv'):
    global log_data
    while not stop_logging.is_set() or log_data:  # Continue until function is done and data is logged
        with lock:
            if log_data:
                with open(filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    while log_data:
                        writer.writerow(log_data.pop(0))  # Write and remove data from the list

        time.sleep(0.01)  # short delay for other threads
    print("log to csv: COMPLETE")




def read_motor():
    global running
    running=True
    M1 = cm.CanMotorController('can0',25,"GIM8108")
    M1.enable_motor()
    M1.set_zero_position()
    print("__________STARTING LOG__________")
    pos=0
    kp=0
    kd=0
    while running:

        # can_id, can_dlc, data = M1._recv_can_frame()
        # positionRawValue, velocityRawValue, currentRawValue = M1.decode_motor_status(data)
        # posdeg,veldeg,curr = M1.convert_raw_to_physical_rad( positionRawValue, velocityRawValue, currentRawValue)
        
        posdeg,veldeg,curr=M1.send_deg_command(pos, 0, kp, kd, 0)

        print(f"ID: Position: {posdeg} rads Velocity: {veldeg} rad/s Current: {curr} amps")
        time.sleep(0.01)


    M1.disable_motor()
    

    






# Create and start the threads
log_25 = threading.Thread(target=read_motor)



log_25 .start()

# Function to stop the thread when a key is pressed
def listen_for_exit():
    global exit_thread
    print("Press 'q' to stop the thread.")
    keyboard.wait('q')  # Wait until 'q' is pressed
    exit_thread = True

# Start the key listener in the main thread
listen_for_exit()


# Join the threads to the main thread
log_25.join()


print("Threads closed successfully.")
