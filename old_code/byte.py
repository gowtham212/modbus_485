decimal_value = 1092264 # output = 0010AAA8

hex_value = hex(decimal_value)
print("Hexadecimal value using hex():", hex_value)
hex_value = format(decimal_value, 'X')
print("Hexadecimal value using format():", hex_value)

# hex_value = hex_value[2:] # Remove the "0x" prefix
# hex_value = hex_value.zfill(4) # Pad with leading zeros if necessary
msb = hex_value[:2]  # Most significant byte
lsb = hex_value[2:]  # Least significant byte

print("Hexadecimal value:", hex_value)
print("MSB:", msb)
print("LSB:", lsb)

print(bytes.fromhex(msb), bytes.fromhex(lsb))