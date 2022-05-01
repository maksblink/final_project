from random import randint


def operation(x, y, operator):
    try:
        process = x.split(',')
        a = process[0]
        b = process[1]

        process = y.split(',')
        c = process[0]
        d = process[1]
    except IndexError:
        print("Bad form of range.")
        print("")
        main()

    points = 0
    rounds = 0

    while True:
        rounds += 1
        try:
            first = randint(int(a), int(b))
            second = randint(int(c), int(d))
        except ValueError:
            print("Bad form of range.")
            print("")
            main()

        result = evaluate_operation(first, second, operator)

        answer_special = input(f"What is {first} {result[1]} {second}: ")
        if answer_special == "":
            continue
        elif answer_special == "stop":
            rounds -= 1
            print(
                f"This is your {rounds} round, your score is {points}, you were correct {precision(rounds, points)}"
                "% of the time.")
            print("")
            break
        elif result[0] == int(answer_special):
            points += 1
            print("Good.")
            print(
                f"This is your {rounds} round, your score is {points}, you were correct {precision(rounds, points)}"
                "% of the time.")
        else:
            print(f"Bad, correct answer is {result[0]}.")
            print(
                f"This is your {rounds} round, your score is {points}, you were correct {precision(rounds, points)}"
                "% of the time.")
            print("")
            break


def validate_range(x, default_value):
    if x == "" or x is None:
        x = default_value
    return x


def precision(p, r):
    try:
        return round(r / p * 100, 2)
    except ZeroDivisionError:
        return 0.0


def validate_operation(answer):
    if answer in ["+", "-", "*", "/", "%"]:
        return True
    else:
        print("Bad operation.")
        print("")
        return False


def evaluate_operation(arg1, arg2, op):
    if op == "+":
        return [arg1 + arg2, "+"]
    elif op == "-":
        return [arg1 - arg2, "-"]
    elif op == "*":
        return [arg1 * arg2, "*"]
    elif op == "/":
        return [arg1 / arg2, "/"]
    elif op == "%":
        return [arg1 % arg2, "%"]


def main():
    while True:
        print("NEW GAME")
        print("Enter one of the +, -, *, /, % signs, to choose what operation you want to train.")
        operator = input("What you want to do?: ")
        print("Now enter the range of numbers you want to focus on,"
              " it must be in format <x,y> where x is the minimum and y is the maximum.")

        range1 = input("Enter the range of first number: ")
        range2 = input("Enter the range of second number: ")
        range1 = validate_range(range1, '1,10')
        range2 = validate_range(range2, '1,10')

        if validate_operation(operator):
            operation(range1, range2, operator)


main()
