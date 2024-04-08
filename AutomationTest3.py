import time
import subprocess
import base64
import zlib
import os
from picamera2 import Picamera2, Preview

# Install Dependencies
subprocess.run(['sudo', 'apt', 'update'])
subprocess.run(['sudo', 'apt', 'install', '-y', 'libraspberrypi0', 'libraspberrypi-dev'])

# Enable Camera
subprocess.run(['sudo', 'raspi-config', 'nonint', 'do_camera', '0'])

# Create an instance of Picamera2
picam2 = Picamera2()

# Create preview configuration
preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
picam2.configure(preview_config)

# Start the preview
picam2.start_preview(Preview.QTGL)

# Start capturing
picam2.start()
time.sleep(10)

# Increment image numbers
image_number = 1
while os.path.exists(f"./images/pictureperfect{image_number}.jpg"):
    image_number += 1

# Capture a file
image_file = f"./images/pictureperfect{image_number}.jpg"
metadata = picam2.capture_file(image_file)
print(metadata)

# Convert image to base64 string
with open(image_file, "rb") as file:
    image_data = file.read()
image_string = base64.b64encode(image_data).decode('utf-8')

# Compress the image string
compressed_data = zlib.compress(image_string.encode('utf-8'))

# Increment file numbers
file_number = 1
while os.path.exists(f"./strings/image_string_{file_number}.txt"):
    file_number += 1

# Save the string and compressed string to files
string_file = f"./strings/image_string_{file_number}.txt"
compressed_file = f"./compressed/compressed_data_{file_number}.txt"

with open(string_file, "w") as file:
    file.write(image_string)

with open(compressed_file, "wb") as file:
    file.write(compressed_data)

# Close the camera
picam2.close()