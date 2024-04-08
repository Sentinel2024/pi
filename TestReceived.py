import serial

serial_port = '/dev/serial0'  # Update with the correct serial port
baud_rate = 9600

ser = serial.Serial(serial_port, baud_rate)

while True:
    if ser.in_waiting > 0:
        received_data = ser.readline().decode().strip()
        print("Received data:", received_data)