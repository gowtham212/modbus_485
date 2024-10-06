#!/usr/bin/env python3
import serial
import time


def calculate_checksum(message):
    """
    Calculate the Modbus checksum for the given message.
    """
    crc = 0xFFFF
    for byte in message:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder="little")


def send_message(serial_port, message):
    """Send message over the serial port and wait for response."""
    serial_port.write(message)
    time.sleep(0.1)
    response = serial_port.read_all()  # Read the response from the serial port
    return response


def mode_of_operation(serial_port):
    # Define the Modbus message components for Operation_mode
    id_op = 0x01
    function_code_op = 0x06
    address_op = 0x3500
    data_op = 0x0003

    # Construct the Modbus message for Operation_mode
    message_op = (
        bytes([id_op, function_code_op])
        + address_op.to_bytes(2, byteorder="big")
        + data_op.to_bytes(2, byteorder="big")
    )

    # Calculate the checksum for Operation_mode
    checksum_op = calculate_checksum(message_op)

    # Combine message and checksum for Operation_mode
    message_with_checksum_op = message_op + checksum_op

    # Send the Modbus message for Operation_mode
    response = send_message(serial_port, message_with_checksum_op)
    print("Operation mode set response:", response)


def enable_function(serial_port):
    # Define the Modbus message components for Controlword
    id_cw = 0x01
    function_code_cw = 0x06
    address_cw = 0x3100
    data_cw = 0x000F

    # Construct the Modbus message for Controlword
    message_cw = (
        bytes([id_cw, function_code_cw])
        + address_cw.to_bytes(2, byteorder="big")
        + data_cw.to_bytes(2, byteorder="big")
    )

    # Calculate the checksum for Controlword
    checksum_cw = calculate_checksum(message_cw)

    # Combine message and checksum for Controlword
    message_with_checksum_cw = message_cw + checksum_cw

    # Send the Modbus message for Controlword
    response = send_message(serial_port, message_with_checksum_cw)
    print("Enable function response:", response)


def disable_function(serial_port):
    # Define the Modbus message components for Controlword
    id_cw = 0x01
    function_code_cw = 0x06
    address_cw = 0x3100
    data_cw = 0x0006

    # Construct the Modbus message for Controlword
    message_cw = (
        bytes([id_cw, function_code_cw])
        + address_cw.to_bytes(2, byteorder="big")
        + data_cw.to_bytes(2, byteorder="big")
    )

    # Calculate the checksum for Controlword
    checksum_cw = calculate_checksum(message_cw)

    # Combine message and checksum for Controlword
    message_with_checksum_cw = message_cw + checksum_cw

    # Send the Modbus message for Controlword
    response = send_message(serial_port, message_with_checksum_cw)
    print("Disable function response:", response)


def polarity_forward_function(serial_port):
    # Define the Modbus message components for Controlword
    id_cw = 0x01
    function_code_cw = 0x06
    address_cw = 0x4700
    data_cw = 0x0000

    # Construct the Modbus message for Controlword
    message_cw = (
        bytes([id_cw, function_code_cw])
        + address_cw.to_bytes(2, byteorder="big")
        + data_cw.to_bytes(2, byteorder="big")
    )

    # Calculate the checksum for Controlword
    checksum_cw = calculate_checksum(message_cw)

    # Combine message and checksum for Controlword
    message_with_checksum_cw = message_cw + checksum_cw

    # Send the Modbus message for Controlword
    response = send_message(serial_port, message_with_checksum_cw)
    print("Forward polarity response:", response)


def polarity_reverse_function(serial_port):
    # Define the Modbus message components for Controlword
    id_cw = 0x01
    function_code_cw = 0x06
    address_cw = 0x4700
    data_cw = 0x0001

    # Construct the Modbus message for Controlword
    message_cw = (
        bytes([id_cw, function_code_cw])
        + address_cw.to_bytes(2, byteorder="big")
        + data_cw.to_bytes(2, byteorder="big")
    )

    # Calculate the checksum for Controlword
    checksum_cw = calculate_checksum(message_cw)

    # Combine message and checksum for Controlword
    message_with_checksum_cw = message_cw + checksum_cw

    # Send the Modbus message for Controlword
    response = send_message(serial_port, message_with_checksum_cw)
    print("Reverse polarity response:", response)


def target_speed(serial_port, rpm):
    # Limit RPM to 3000 if it exceeds the maximum limit
    if rpm > 3000:
        print(
            f"Warning: RPM value {rpm} exceeds the maximum limit. Setting RPM to 3000."
        )
        rpm = 2000  # Set RPM to the maximum limit of 3000

    # Define the Modbus message components
    id = 0x01
    function_code = 0x10
    address = 0x6F00
    data_length = 0x0002

    # Convert RPM to a Modbus-compatible value
    decimal_number = int(2730.66 * rpm)

    # Split the value into two 16-bit parts (since Modbus registers are 16-bit)
    data_part1 = decimal_number & 0xFFFF
    data_part2 = (decimal_number >> 16) & 0xFFFF

    # Construct the Modbus message
    message = (
        bytes([id, function_code])
        + address.to_bytes(2, byteorder="big")
        + data_length.to_bytes(2, byteorder="big")
    )
    message += (data_length * 2).to_bytes(1, byteorder="big")
    message += data_part1.to_bytes(2, byteorder="big")
    message += data_part2.to_bytes(2, byteorder="big")

    # Calculate the checksum
    checksum = calculate_checksum(message)

    # Combine message and checksum
    message_with_checksum = message + checksum

    # Send the Modbus message
    response = send_message(serial_port, message_with_checksum)
    print("Target speed response:", response)


def acceleration(serial_port):
    # Define the Modbus message components
    id = 0x01
    function_code = 0x10
    address = 0x2960
    num_registers = 0x0002  # Writing two registers
    data_length_bytes = 0x04  # Two 16-bit registers = 4 bytes of data

    # Acceleration data
    rps = 100  # Modify this to your desired acceleration rate
    decimal_value = int(1 * rps * 1)

    # Convert the decimal value to two 16-bit parts
    data_part1 = decimal_value & 0xFFFF
    data_part2 = (decimal_value >> 16) & 0xFFFF

    # Construct the Modbus message
    message = (
        bytes([id, function_code])
        + address.to_bytes(2, byteorder="big")
        + num_registers.to_bytes(2, byteorder="big")
        + bytes([data_length_bytes])
        + data_part1.to_bytes(2, byteorder="big")
        + data_part2.to_bytes(2, byteorder="big")
    )

    # Calculate the checksum
    checksum = calculate_checksum(message)

    # Combine message and checksum
    message_with_checksum = message + checksum

    # Send the Modbus message
    response = send_message(serial_port, message_with_checksum)
    print("Acceleration response:", response)


def deacceleration(serial_port):
    # Define the Modbus message components
    id = 0x01
    function_code = 0x10
    address = 0x2970
    num_registers = 0x0002  # Writing two registers
    data_length_bytes = 0x04  # Two 16-bit registers = 4 bytes of data

    # Deacceleration data
    rps = 100  # Modify this to your desired deacceleration rate
    decimal_value = int(1 * rps * 1)

    # Convert the decimal value to two 16-bit parts
    data_part1 = decimal_value & 0xFFFF
    data_part2 = (decimal_value >> 16) & 0xFFFF

    # Construct the Modbus message
    message = (
        bytes([id, function_code])
        + address.to_bytes(2, byteorder="big")
        + num_registers.to_bytes(2, byteorder="big")
        + bytes([data_length_bytes])
        + data_part1.to_bytes(2, byteorder="big")
        + data_part2.to_bytes(2, byteorder="big")
    )

    # Calculate the checksum
    checksum = calculate_checksum(message)

    # Combine message and checksum
    message_with_checksum = message + checksum

    # Send the Modbus message
    response = send_message(serial_port, message_with_checksum)
    print("Deacceleration response:", response)


# Configure the serial connection
serial_port = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=38400,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1,
)

# Use the functions
mode_of_operation(serial_port)
time.sleep(0.5)
acceleration(serial_port)
time.sleep(0.5)
deacceleration(serial_port)
time.sleep(0.5)
# polarity_reverse_function(serial_port)
# enable_function(serial_port)
# time.sleep(0.5)
# disable_function(serial_port)
# polarity_forward_function(serial_port)

target_speed(serial_port, 10000)  # Pass 100 RPM
time.sleep(0.5)
enable_function(serial_port)

# time.sleep(5)
# disable_function(serial_port)

# Close the serial connection
serial_port.close()
