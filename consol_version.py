from random import randint


def operation(x, y, operator):
    process = x.split(',')
    a = process[0]
    b = process[1]

    process = y.split(',')
    c = process[0]
    d = process[1]

    points = 0
    rounds = 0

    while True:
        rounds += 1
        first = randint(int(a), int(b))
        second = randint(int(c), int(d))
        result = evaluate_operation(first, second, operator)

        answer_special = input(f"What is {first} * {second}: ")
        if answer_special == "stop":
            print(f"This is your {rounds} round, your score is {points}")
            break
        elif result == int(answer_special):
            points += 1
            print("Good")
            print(f"This is your {rounds} round, your score is {points}")
        else:
            print("Bad")
            print(f"This is your {rounds} round, your score is {points}")
            return first * second


def validate_range(x, default_value):
    if x == "" or x is None:
        x = default_value
    return x


def validate_operation(answer):
    return answer in ["+", "-", "*", "/", "%"]


def evaluate_operation(arg1, arg2, op):
    if op == "+":
        return arg1 + arg2
    elif op == "-":
        pass
    elif op == "*":
        return arg1 * arg2
    elif op == "/":
        pass
    elif op == "%":
        pass


while True:
    operator = input("What you want to do?: ")

    range1 = input("Enter the range of first number: ")
    range2 = input("Enter the range of second number: ")
    range1 = validate_range(range1, '1,10')
    range2 = validate_range(range2, '1,10')
    # val3 = input("Enter the third value: ")

    if not validate_operation(operator):
        continue
    operation(range1, range2, operator)
