from pymodbus.client import ModbusSerialClient

# basic code for forward ,enable disable and operation mode code

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


def mode_of_operation():
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
    client.write_registers(address_op, [data_op], unit=station_no)


def enable_function():
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
    client.write_registers(address_cw, [data_cw], unit=station_no)

    # Close the Modbus client connection


def disable_function():
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
    client.write_registers(address_cw, [data_cw], unit=station_no)


def polarity_forward_function():
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
    client.write_registers(address_cw, [data_cw], unit=station_no)
    print("forward_polarity")


def polarity_reverse_function():
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
    client.write_registers(address_cw, [data_cw], unit=station_no)
    print("reverese_polarity")


def target_speed():
    # Define the Modbus message components
    id = 0x01
    function_code = 0x10
    address = 0x6F00
    data_length = 0x0002
    rpm = 2999
    decimal_number = int(2730.66 * rpm)  # Convert the result to an integer
    hex_number = hex(decimal_number)
    print(hex_number)
    hex_value = int(hex_number, 16)
    print(hex_value)

    data_part1 = hex_value & 0xFFFF
    data_part2 = (hex_value >> 16) & 0xFFFF

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
    client.write_registers(address, [data_part1, data_part2], unit=station_no)


def acceleration():
    # Define the Modbus message components  ##DEC=[(RPS/S*65536*encoder resolution)/4000000]=rps*163.84
    id = 0x01
    function_code = 0x10
    address = 0x2960
    data_length = 0x0002
    rps = 100
    decimal_value = int(1 * rps * 1)
    print("Decimal value_rps:", decimal_value)

    # Convert the decimal value to hexadecimal string
    hex_value = format(decimal_value, "04X")

    # Ensure the hexadecimal string is four characters long
    hex_value = hex_value.zfill(4)

    # Split the hexadecimal string into two parts
    part1 = "0x" + hex_value[:4]
    part2 = hex_value[4:]

    # Convert the hexadecimal parts to integers
    data_part1 = int(part1, 0)
    data_part2 = int(part2, 16) if part2 else 0

    # Construct the Modbus message
    message = (
        bytes([id, function_code])
        + address.to_bytes(2, byteorder="big")
        + data_length.to_bytes(2, byteorder="big")
    )

    # Add data to the message
    message += data_part1.to_bytes(2, byteorder="big")
    message += data_part2.to_bytes(2, byteorder="big")

    # Calculate the checksum
    checksum = calculate_checksum(message)

    # Combine message and checksum
    message_with_checksum = message + checksum

    # Send the Modbus message
    client.write_registers(address, [data_part1, data_part2], unit=station_no)


def deacceleration():
    # Define the Modbus message components  ##DEC=[(RPS/S*65536*encoder resolution)/4000000]=rps*163.84
    id = 0x01
    function_code = 0x10
    address = 0x2970
    data_length = 0x0002
    rps = 1
    decimal_value = int(1 * rps * 1)
    print("Decimal value_rps:", decimal_value)

    # Convert the decimal value to hexadecimal string
    hex_value = format(decimal_value, "04X")

    # Ensure the hexadecimal string is four characters long
    hex_value = hex_value.zfill(4)

    # Split the hexadecimal string into two parts
    part1 = "0x" + hex_value[:4]
    part2 = hex_value[4:]

    # Convert the hexadecimal parts to integers
    data_part1 = int(part1, 0)
    data_part2 = int(part2, 16) if part2 else 0

    # Construct the Modbus message
    message = (
        bytes([id, function_code])
        + address.to_bytes(2, byteorder="big")
        + data_length.to_bytes(2, byteorder="big")
    )

    # Add data to the message
    message += data_part1.to_bytes(2, byteorder="big")
    message += data_part2.to_bytes(2, byteorder="big")

    # Calculate the checksum
    checksum = calculate_checksum(message)

    # Combine message and checksum
    message_with_checksum = message + checksum

    # Send the Modbus message
    client.write_registers(address, [data_part1, data_part2], unit=station_no)


# Configure Modbus client
client = ModbusSerialClient(
    method="rtu",
    port="/dev/ttyUSB0",
    baudrate=38400,
    stopbits=1,
    parity="N",
    bytesize=8,
)
client.connect()

# Define the station number
station_no = 1

print("operation_function")
mode_of_operation()
# acceleration()
# deacceleration()
target_speed()

polarity_forward_function()
print("forward")
print("enable_function")
enable_function()

# time.sleep(30)
# print("disable_function")
# disable_function()

# time.sleep(10)
# polarity_reverse_function()
# print("reverse")
# print("enable_function")
# enable_function()

# time.sleep(30)
# print("disable_function")
# disable_function()
client.close()
