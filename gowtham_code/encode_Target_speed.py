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
    time.sleep(0.1)  # Wait for the response
    response = serial_port.read_all()  # Read the response from the serial port
    return response


def read_encoder_value(serial_port):
    # Define the Modbus message components for reading the encoder value
    id = 0x01
    function_code = 0x03
    address = 0x3700  # Correct address for encoder value
    num_registers = 0x0002  # Reading 2 registers (16 bits each)

    # Construct the Modbus request message
    message = (
        bytes([id, function_code])
        + address.to_bytes(2, byteorder="big")
        + num_registers.to_bytes(2, byteorder="big")
    )

    # Calculate the checksum
    checksum = calculate_checksum(message)

    # Combine message and checksum
    message_with_checksum = message + checksum

    # Send the Modbus request and read the response
    response = send_message(serial_port, message_with_checksum)

    # Log the raw response for debugging
    print("Raw encoder response:", response)

    # Validate response length
    if len(response) < 7:  # Minimum length for a valid response (5 header + 2 data)
        print("Invalid response for encoder reading:", response)
        return None

    # Unpack the response
    try:
        # Check if the response contains the necessary data
        if (
            len(response) >= 7
        ):  # Must have at least 7 bytes (slave ID + function code + byte count + data + CRC)
            # Extract the encoder value (assuming two 16-bit registers for a 32-bit value)
            low_value = int.from_bytes(response[3:5], byteorder="big")  # Low 16 bits
            high_value = int.from_bytes(response[5:7], byteorder="big")  # High 16 bits
            # Combine to form a full 32-bit value
            value = (high_value << 16) + low_value  # Concatenate high and low parts
            print(f"Parsed encoder value: {value}")  # Log the parsed value

            return value
        else:
            print("Response does not contain sufficient data for encoder value.")
            return None
    except Exception as e:
        print(f"Error parsing encoder value: {e}")
        return None


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
    address = 0x2980
    num_registers = 0x0002  # Writing two registers
    data_length_bytes = 0x04  # Two 16-bit registers = 4 bytes of data

    # Deceleration data
    rps = 100  # Modify this to your desired deceleration rate
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


def main():
    # Replace '/dev/ttyUSB0' with your serial port and set the appropriate baud rate
    serial_port = serial.Serial("/dev/ttyUSB0", baudrate=38400, timeout=1)

    try:
        # Set operation mode
        mode_of_operation(serial_port)

        # Enable function
        enable_function(serial_port)

        # Set target speed
        target_speed(serial_port, 100)

        # Set acceleration
        acceleration(serial_port)

        # Set deacceleration
        deacceleration(serial_port)

        # Set forward polarity
        polarity_forward_function(serial_port)

        # Continuously read the encoder value
        while True:
            encoder_value = read_encoder_value(serial_port)
            if encoder_value is not None:
                print("Current Encoder Value:", encoder_value)
            time.sleep(0.5)  # Adjust the delay as needed (0.5 seconds in this case)

        # Optionally set reverse polarity
        # polarity_reverse_function(serial_port)

        # Optionally disable function
        # disable_function(serial_port)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Interrupted by user. Stopping...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        serial_port.close()


if __name__ == "__main__":
    main()
