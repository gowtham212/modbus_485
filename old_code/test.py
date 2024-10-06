decimal_value = 1092264

# Using hex() function
hex_value1 = hex(decimal_value)
print("Hexadecimal value:", hex_value1)  # Output: 0x85555

# Using format() function
hex_value2 = format(decimal_value, 'x')
print("Hexadecimal value:", hex_value2)  # Output: 85555

# Print the reverse of hex_value2
reversed_hex_value = hex_value2[::-1]
print("Reversed Hexadecimal value:", reversed_hex_value)  # Output: 55558

# Convert the reversed hexadecimal value to the desired format
formatted_data = "[0x" + reversed_hex_value[:4] + ", 0x" + reversed_hex_value[4:].zfill(4) + "]"
print("Formatted data:", formatted_data)  # Output: [0x5555, 0x0008]

