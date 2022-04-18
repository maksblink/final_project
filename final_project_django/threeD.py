def length(coordinate1, coordinate2):
    if (coordinate1 > 0 and coordinate2 > 0) or (coordinate1 < 0 and coordinate2 < 0):
        return abs(coordinate1 - coordinate2)
    else:
        return abs(coordinate1) + abs(coordinate2)


def distance(first, second):
    x1 = first[0]
    y1 = first[1]
    z1 = first[2]
    x2 = second[0]
    y2 = second[1]
    z2 = second[2]

    xLong = length(x1, x2)
    yLong = length(y1, y2)
    zLong = length(z1, z2)
    flat_diagonal = ((xLong ** 2) + (yLong ** 2)) ** 0.5

    final_diagonal = ((zLong ** 2) + (flat_diagonal ** 2)) ** 0.5

    # print(f"long x: {xLong}")
    # print(f"long y: {yLong}")
    # print(f"long z: {zLong}")
    # print(f"flat diagonal: {flat_diagonal} (less important)")
    # print(f"final diagonal: {final_diagonal}")
    return final_diagonal


print(distance([99, 1, 0], [-120, 87, 121]))


########################################################################################################################


def statistic(scope_of_space):
    checked_positions = 0
    integer_positions = 0

    number_of_iterations = 0
    while scope_of_space[0] <= scope_of_space[1]:
        number_of_iterations += 1
        scope_of_space[0] += 1

    for x1 in range(number_of_iterations):
        print("#####")
        for y1 in range(number_of_iterations):
            print("@")
            for z1 in range(number_of_iterations):

                for x2 in range(number_of_iterations):

                    for y2 in range(number_of_iterations):

                        for z2 in range(number_of_iterations):
                            checked_positions += 1
                            val = distance([x1, y1, z1], [x2, y2, z2])
                            if val == int(val):
                                integer_positions += 1

    print(f"number of iterations: {number_of_iterations}")
    print(f"statistic: {integer_positions * 100 / checked_positions} %")
    return {"checked positions:": checked_positions, "integer positions:": integer_positions}


print(statistic([-10, 5]))
