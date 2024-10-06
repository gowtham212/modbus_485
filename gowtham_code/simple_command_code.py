import serial
import time

# Define RS485 communication parameters
port = "/dev/ttyUSB0"  # Change to your correct port if needed
baudrate = 38400
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE
bytesize = serial.EIGHTBITS
timeout = 1  # Timeout in seconds

# Initialize the serial connection
ser = serial.Serial(
    port=port,
    baudrate=baudrate,
    parity=parity,
    stopbits=stopbits,
    bytesize=bytesize,
    timeout=timeout,
)


# Function to send hexadecimal command
def send_command(command_hex):
    # Convert hex string to bytes
    command_bytes = bytes.fromhex(command_hex)
    ser.write(command_bytes)
    print(f"Sent: {command_hex}")
    time.sleep(0.1)  # Add a small delay to ensure transmission


# Commands (hex string)
operation_mode = "010635000003C607"
set_200_rpm = "01106F00000204555500081A47"
set_0_rpm = "01106F00000204000000001A5D"
enable = "01063100000FC732"
disable = "0106310000060734"

# Send commands
try:
    send_command(operation_mode)  # Send operation mode command
    time.sleep(0.5)
    send_command(set_200_rpm)  # Set motor to 200 rpm
    time.sleep(0.5)
    # send_command(set_0_rpm)  # Set motor to 0 rpm
    send_command(enable)  # Enable motor
    time.sleep(0.5)
    send_command(set_0_rpm)  # Set motor to 0 rpm
    time.sleep(0.5)
    send_command(disable)  # Disable motor

finally:
    ser.close()  # Close the serial connection when done
    print("Serial connection closed.")
