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

        # Close the Modbus client connection

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

            # Close the Modbus client connection

        # Configure Modbus client
client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, stopbits=1, parity='N', bytesize=8)
client.connect()

# Define the station number
station_no = 1
print("disable_function")
disable_function()
client.close()
