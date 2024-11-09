#Can Header dict



CAN_send_header = {
    "CAN_CMD_MOTORID"   : 0b001,	# request for resetting a motor's CAN ID
    "CAN_CMD_SOFTSTART" : 0b010	# request for soft start
}

#  message header definitions; the leading three bits are the message identifier,
#  the rest are the message contents. These are for outgoing messages only

CAN_receive_header={
    "CAN_MSG_READY  " : 0b000,     # message to indicate the board is ready to do things
    "CAN_MSG_BATTERY" : 0b001,  # header to indicate the message contains the battery voltage
    "CAN_MSG_CONFIRM" : 0b011,  # message to confirm that the requested action has been done
    "CAN_MSG_ERROR  " : 0b111		# message to indicate an error
} 