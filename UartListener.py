import serial
import subprocess
import base64
import zlib
import os
import time
from picamera2 import Picamera2, Preview

# Enable Camera
subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_camera', '0'])

# Create an instance of Picamera2
picam2 = Picamera2()

# Create preview configuration
preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
picam2.configure(preview_config)

# Serial Settings
serial_port = '/dev/serial0'  # Update with the correct serial port
baud_rate = 9600  # Update with the baud rate used by the ESP

# Open the serial port
ser = serial.Serial(serial_port, baud_rate)

# Wait for the serial port to be ready
time.sleep(2)

# Function to execute the capture image task
def capture_image():
    # Start the preview
    picam2.start_preview(Preview.QTGL)
    time.sleep(2)

    # Capture a file with a timestamp in the name
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    image_file = f"image_{timestamp}.jpg"
    metadata = picam2.capture_file(image_file)
    print(metadata)

    # Convert image to base64 string
    with open(image_file, "rb") as file:
        image_data = file.read()
    image_string = base64.b64encode(image_data).decode('utf-8')

    # Compress the image string
    compressed_data = zlib.compress(image_string.encode('utf-8'))

    # Increment file numbers for string and compressed data files
    file_number = 1
    while os.path.exists(f"image_string_{file_number}.txt"):
        file_number += 1

    # Save the string and compressed string to files
    string_file = f"image_string_{file_number}.txt"
    compressed_file = f"compressed_data_{file_number}.txt"

    with open(string_file, "w") as file:
        file.write(image_string)

    with open(compressed_file, "wb") as file:
        file.write(compressed_data)

    # Stop the preview
    picam2.stop_preview()

# Read and process incoming UART messages
while True:
    if ser.in_waiting > 0:
        # Read the incoming message
        message = ser.readline().decode('utf-8').strip()

        # Process the message
        if message == 'capture_image':
            capture_image()