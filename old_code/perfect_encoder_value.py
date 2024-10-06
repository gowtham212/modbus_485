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



def position_actual_values():
    # Define the Modbus message components
    id = 0x01
    function_code = 0x03
    address = 0x3710
    data_length = 0x0004

    # Construct the Modbus message
    message = bytes([id, function_code]) + address.to_bytes(2, byteorder='big') + data_length.to_bytes(2, byteorder='big')

    # Send the Modbus message and receive response
    response = client.read_holding_registers(address, data_length, unit=station_no)
    print("response", response)

    if response.isError():
        print("Failed to read the registers.")
    else:
        # Extract the registers from the response
        registers = response.registers

        # Combine the registers into a 32-bit integer (little-endian byte order)
        value = (registers[1] << 16) | registers[0]

        print("Value (Decimal):", value)
while 1:
       client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, stopbits=1, parity='N', bytesize=8)
       client.connect()
       # Define the station number
       station_no = 1
       position_actual_values()
       time.sleep(0.1)



client.close()