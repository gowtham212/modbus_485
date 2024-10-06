# decimal_value = 1092264
# data_part1 = format(decimal_value & 0xFFFF, '04X')
# data_part2 = format(8, '04X')

# print("data_part1 =", "0x" + data_part1)
# print("data_part2 =", "0x" + data_part2)
# print(type(data_part1))
# print(type(data_part2))
# # 
decimal_value = 1092264
data_part1 = format(decimal_value & 0xFFFF, '04X')
data_part2 = format(8, '04X')

print("data_part1 =", "0x" + data_part1)
print("data_part2 =", "0x" + data_part2)
print(type(data_part1))
print(type(data_part2))

data_part1 = (data_part1, 16)
data_part2 = (data_part2, 16)

print("data_part1 (int) =", data_part1)
print("data_part2 (int) =", data_part2)

print(type(data_part1))
print(type(data_part2))

data_part1 = (data_part1[0])
data_part2 = (data_part2[0])

print("data_part1 =", data_part1)
print("data_part2 =", data_part2)

print(type(data_part1))
print(type(data_part2))

