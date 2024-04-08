import serial
import time
import subprocess
import os

if __name__ == '__main__':
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Try opening '/dev/ttyUSB0'
    except serial.SerialException:
        try:
            ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)  # Try opening '/dev/ttyS0' as an alternative
        except serial.SerialException:
            print("Failed to open serial port. Make sure the device is connected.")
            exit(1)

    ser.flush()

    while True:
        if ser.in_waiting > 0:
            received_data = ser.readline().decode('utf-8').rstrip()
            print("Received:", received_data)
            
            if received_data == 'capture image':
                # Replace 'script_name.py' with the name of your script file
                script_path = os.path.join(os.path.dirname(__file__), 'AutomationTest3.py')
                
                try:
                    # Execute the script using the subprocess module
                    subprocess.run(['python3', script_path])
                    print('Script executed successfully')
                except Exception as e:
                    print('Error executing script:', str(e))
        else:
            print("No data received")

        time.sleep(1)  # Delay of 1 second