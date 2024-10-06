import serial
import time


# Function to calculate Modbus CRC checksum
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


class MotorController:
    def __init__(self, port="/dev/ttyUSB0", baudrate=38400, timeout=1):
        """
        Initialize the serial connection with RS485 communication parameters
        """
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout,
        )

    def send_modbus_message(self, message):
        """
        Send a Modbus message with CRC checksum through serial port
        """
        checksum = calculate_checksum(message)
        message_with_checksum = message + checksum
        self.ser.write(message_with_checksum)
        print(f"Sent: {message_with_checksum.hex()}")
        time.sleep(0.1)  # Small delay for transmission

    def mode_of_operation(self):
        """
        Enable operation mode of the motor using Modbus protocol
        """
        id_op = 0x01  # Device ID
        function_code_op = 0x06  # Function code for 'Write Single Register'
        address_op = 0x3500  # Register address for operation mode
        data_op = 0x0003  # Data to write (set operation mode)

        # Create the Modbus message (without checksum)
        message_op = (
            bytes([id_op, function_code_op])
            + address_op.to_bytes(2, byteorder="big")
            + data_op.to_bytes(2, byteorder="big")
        )

        # Send the message with checksum
        self.send_modbus_message(message_op)

    def enable_motor(self):
        """
        Enable the motor through Modbus command
        """
        id_enable = 0x01  # Device ID
        function_code_enable = 0x06  # Function code for 'Write Single Register'
        address_enable = 0x3100  # Register address for enabling motor
        data_enable = 0x000F  # Data to write (enable motor)

        # Create the Modbus message (without checksum)
        message_enable = (
            bytes([id_enable, function_code_enable])
            + address_enable.to_bytes(2, byteorder="big")
            + data_enable.to_bytes(2, byteorder="big")
        )

        # Send the message with checksum
        self.send_modbus_message(message_enable)

    def disable_motor(self):
        """
        Disable the motor through Modbus command
        """
        id_disable = 0x01  # Device ID
        function_code_disable = 0x06  # Function code for 'Write Single Register'
        address_disable = 0x3100  # Register address for disabling motor
        data_disable = 0x0006  # Data to write (disable motor)

        # Create the Modbus message (without checksum)
        message_disable = (
            bytes([id_disable, function_code_disable])
            + address_disable.to_bytes(2, byteorder="big")
            + data_disable.to_bytes(2, byteorder="big")
        )

        # Send the message with checksum
        self.send_modbus_message(message_disable)

    def close(self):
        """
        Close the serial connection
        """
        self.ser.close()
        print("Serial connection closed.")


# Main control logic
if __name__ == "__main__":
    motor_controller = MotorController()

    try:
        motor_controller.mode_of_operation()  # Set motor to operation mode
        time.sleep(0.5)

        motor_controller.enable_motor()  # Enable the motor
        time.sleep(0.5)

        # Optionally, disable the motor after some time
        # motor_controller.disable_motor()
    finally:
        motor_controller.close()  # Ensure the serial connection is closed
