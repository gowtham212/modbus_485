from pymodbus.client.sync import ModbusSerialClient
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
    return crc.to_bytes(2, byteorder='little')


def mode_of_operation():
    # Define the Modbus message components for Operation_mode
    id_op = 0x01
    function_code_op = 0x06
    address_op = 0x3500
    data_op = 0x0003

    # Construct the Modbus message for Operation_mode
    message_op = bytes([id_op, function_code_op]) + address_op.to_bytes(2, byteorder='big') + data_op.to_bytes(2, byteorder='big')

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
    message_cw = bytes([id_cw, function_code_cw]) + address_cw.to_bytes(2, byteorder='big') + data_cw.to_bytes(2, byteorder='big')

    # Calculate the checksum for Controlword
    checksum_cw = calculate_checksum(message_cw)

    # Combine message and checksum for Controlword
    message_with_checksum_cw = message_cw + checksum_cw

    # Send the Modbus message for Controlword
    client.write_registers(address_cw, [data_cw], unit=station_no)


def disable_function():
    # Define the Modbus message components for Controlword
    id_cw = 0x01
    function_code_cw = 0x06
    address_cw = 0x3100
    data_cw = 0x0006

    # Construct the Modbus message for Controlword
    message_cw = bytes([id_cw, function_code_cw]) + address_cw.to_bytes(2, byteorder='big') + data_cw.to_bytes(2, byteorder='big')

    # Calculate the checksum for Controlword
    checksum_cw = calculate_checksum(message_cw)

    # Combine message and checksum for Controlword
    message_with_checksum_cw = message_cw + checksum_cw

    # Send the Modbus message for Controlword
    client.write_registers(address_cw, [data_cw], unit=station_no)


def target_speed():
    # Define the Modbus message components
    id = 0x01
    function_code = 0x10
    address = 0x6F00
    data_length = 0x0002
    rpm = 10
    decimal_value = int(2730.66667 * rpm * 1)
    print("Decimal value:", decimal_value)

    # Convert the decimal value to hexadecimal string
    hex_value = format(decimal_value, '04X')

    # Ensure the hexadecimal string is four characters long
    hex_value = hex_value.zfill(4)

    # Split the hexadecimal string into two parts
    part1 = '0x' + hex_value[:4]
    part2 = hex_value[4:]

    # Convert the hexadecimal parts to integers
    data_part1 = int(part1, 0)
    data_part2 = int(part2, 16) if part2 else 0

    # Construct the Modbus message
    message = bytes([id, function_code]) + address.to_bytes(2, byteorder='big') + data_length.to_bytes(2, byteorder='big')

    # Add data to the message
    message += data_part1.to_bytes(2, byteorder='big')
    message += data_part2.to_bytes(2, byteorder='big')

    # Calculate the checksum
    checksum = calculate_checksum(message)

    # Combine message and checksum
    message_with_checksum = message + checksum

    # Send the Modbus message
    client.write_registers(address, [data_part1, data_part2], unit=station_no)


def polarity_forward_function():
            # Define the Modbus message components for Controlword
            id_cw = 0x01
            function_code_cw = 0x06
            address_cw = 0x4700
            data_cw = 0x0000

            # Construct the Modbus message for Controlword
            message_cw = bytes([id_cw, function_code_cw]) + address_cw.to_bytes(2, byteorder='big') + data_cw.to_bytes(2, byteorder='big')

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
            message_cw = bytes([id_cw, function_code_cw]) + address_cw.to_bytes(2, byteorder='big') + data_cw.to_bytes(2, byteorder='big')

            # Calculate the checksum for Controlword
            checksum_cw = calculate_checksum(message_cw)

            # Combine message and checksum for Controlword
            message_with_checksum_cw = message_cw + checksum_cw

            # Send the Modbus message for Controlword
            client.write_registers(address_cw, [data_cw], unit=station_no)
            print("reverese_polarity")




try:
    # Configure Modbus client
    client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, stopbits=1, parity='N', bytesize=8)
    client.connect()

    # Define the station number
    station_no = 1

    print("enable_function")
    enable_function()

    print("mode_of_operation")
    mode_of_operation()

    print("target_speed")
    target_speed()

    time.sleep(10)
    target_speed()

    time.sleep(10)

    print("disable_function")
    disable_function()

    client.close()
except KeyboardInterrupt:
    disable_function()
    print("Keyboard interrupt detected. Exiting...")
