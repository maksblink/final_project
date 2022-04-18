from random import randint

table = []

for i in range(100000):
    x = randint(0, 1)
    table.append(x)

# print("tabela losowan: ", table)

counter_zero = 0
counter_zero_table = []

for i in table:
    if i == 0:
        counter_zero += 1
    else:
        counter_zero_table.append(counter_zero)
        counter_zero = 0

counter_zero_table.append(counter_zero)

counter_one = 0
counter_one_table = []

for i in table:
    if i == 1:
        counter_one += 1
    else:
        counter_one_table.append(counter_one)
        counter_one = 0

counter_one_table.append(counter_one)

print("")

# print("tabela dlugosci powtorzen zer: ", counter_zero_table)
print("największa ilosc powtorzen zer: ", max(counter_zero_table))

print("")

# print("tabela dlugosci powtorzen jedynek: ", counter_one_table)
print("największa ilosc powtorzen jedynek: ", max(counter_one_table))

print("")

bad_luck = pow(2, max(counter_zero_table))
bad_luck_1 = pow(2, max(counter_one_table))

print(bad_luck)
print(bad_luck_1)

print("")

money_1 = pow(2, max(counter_zero_table) + 1) - 1
money_2 = pow(2, max(counter_one_table) + 1) - 1

print("pieniadze_1: ", money_1)
print("pieniadze_2: ", money_2)
