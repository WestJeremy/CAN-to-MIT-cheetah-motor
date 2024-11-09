
sudo ip link set down can0
sudo ip link set down can1


sudo busybox devmem 0x0c303000 32 0x0000C400
sudo busybox devmem 0x0c303008 32 0x0000C454
sudo busybox devmem 0x0c303010 32 0x0000C400
sudo busybox devmem 0x0c303018 32 0x0000C454
sudo modprobe can
sudo modprobe can_raw
sudo modprobe mttcan
# sudo ip link set can0 type can bitrate 1000000 dbitrate 1000000 berr-reporting on fd on
# sudo ip link set can1 type can bitrate 1000000 dbitrate 1000000 berr-reporting on fd on

sudo ip link set can0 type can bitrate 1000000 berr-reporting on fd off
sudo ip link set can1 type can bitrate 1000000 berr-reporting on fd off



sudo ip link set up can0
sudo ip link set up can1

