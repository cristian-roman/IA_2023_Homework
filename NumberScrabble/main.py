import copy

magic_square = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
# player_turn can take value 1 for player 1 or value 2 for player 2


def is_any_line_in_final_state(current_state):
    for i in range(len(current_state[1])):
        k = 0
        for j in range(3):
            if current_state[1][i][j] == 3 - current_state[0]:
                k += 1
        if k == 3:
            return True
    return False


def is_any_column_in_final_state(current_state):
    for j in range(3):
        k = 0
        for i in range(len(current_state[1])):
            if current_state[1][i][j] == 3 - current_state[0]:
                k += 1
        if k == 3:
            return True
    return False


def is_any_diagonal_in_final_state(current_state):
    k = 0
    for i in range(3):
        if current_state[1][i][i] == current_state[0]:
            k += 1
    if k == 3:
        return True
    k = 0
    for i in range(len(current_state[1])):
        if current_state[1][i][3 - i - 1] == 3 - current_state[0]:
            k += 1
    if k == 3:
        return True
    return False


def is_final_state(current_state):
    if (is_any_line_in_final_state(current_state) or is_any_column_in_final_state(current_state)
            or is_any_diagonal_in_final_state(current_state)):
        return True
    else:
        return False


def search_value(value):
    for i in range(3):
        for j in range(3):
            if magic_square[i][j] == value:
                return i, j
    return None


def is_value_already_used(current_state, position):
    if current_state[1][position[0]][position[1]] != 0:
        return True
    return False


def get_next_state(current_state, position):
    temp_state = (3 - current_state[0], copy.deepcopy(current_state[1]), current_state[2])
    temp_state[1][position[0]][position[1]] = current_state[0]
    temp_state_score = get_score_for_state(temp_state, current_state[2])
    return temp_state[0], temp_state[1], current_state[2] - temp_state_score


def is_position_valid(current_state, position):
    if position is None:
        return False
    if is_value_already_used(current_state, position):
        return False
    return True


def is_line_open(i, new_state):
    k = 0
    for j in range(3):
        if new_state[1][i][j] == 0 or new_state[1][i][j] == new_state[0]:
            k += 1
    if k == 3:
        return True
    return False


def is_column_open(j, new_state):
    k = 0
    for i in range(3):
        if new_state[1][i][j] == new_state[0] or new_state[1][i][j] == 0:
            k += 1
    if k == 3:
        return True
    return False


def is_main_diagonal_open(new_state):
    k = 0
    for i in range(3):
        if new_state[1][i][i] == new_state[0] or new_state[1][i][i] == 0:
            k += 1
    if k == 3:
        return True
    return False


def is_secondary_diagonal_open(new_state):
    k = 0
    for i in range(3):
        if new_state[1][i][len(new_state[1]) - i - 1] == new_state[0] or new_state[1][i][len(new_state[1]) - i - 1] == 0:
            k += 1
    if k == 3:
        return True
    return False


def get_score_for_state(new_state, number_of_open_paths_for_previous_state):
    number_of_open_paths = 0
    for i in range(3):
        if is_line_open(i, new_state):
            number_of_open_paths += 1
        if is_column_open(i, new_state):
            number_of_open_paths += 1
    if is_main_diagonal_open(new_state):
        number_of_open_paths += 1
    if is_secondary_diagonal_open(new_state):
        number_of_open_paths += 1
    return number_of_open_paths_for_previous_state - number_of_open_paths


def validate_state(current_state, new_state):
    k = 0
    for i in range(3):
        for j in range(3):
            if current_state[1][i][j] != 0 and current_state[1][i][j] != new_state[1][i][j]:
                return False
            if current_state[1][i][j] == new_state[1][i][j]:
                k += 1
    if k == 9:
        return False
    return True


def minimax(current_state, depth):
    if depth == 0 or is_final_state(current_state):
        return current_state, get_score_for_state(current_state, current_state[2])
    to_return_state = ()
    if current_state[0] == 2:
        value = 100
        for i in range(3):
            for j in range(3):
                new_state = get_next_state(current_state, (i, j))
                if not validate_state(current_state, new_state):
                    continue
                new_state, new_value = minimax(new_state, depth - 1)
                if value > new_value:
                    value = new_value
                    to_return_state = new_state
                    if depth == 3:
                       to_return_state = get_next_state(current_state, (i, j))
    else:
        value = -100
        for i in range(3):
            for j in range(3):
                new_state = get_next_state(current_state, (i, j))
                if not validate_state(current_state, new_state):
                    continue
                new_state, new_value = minimax(new_state, depth - 1)
                if value < new_value:
                    value = new_value
                    to_return_state = new_state
    return to_return_state, value


def get_computers_choice(current_state, new_state):
    for i in range(3):
        for j in range(3):
            if new_state[1][i][j] != 0 and current_state[1][i][j] != new_state[1][i][j]:
                return magic_square[i][j]


def play():
    state = (1, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 8)
    # 1 = who's turn is it to choose a number
    # [[0, 0, 0], [0, 0, 0], [0, 0, 0]] = the current state of the game
    # 8 = the number of open paths for the previous state
    while not is_final_state(state):
        if state[0] == 1:
            print("Enter your input: ")
            value = int(input())

            position = search_value(value)
            if not is_position_valid(state, position):
                print("Your input is not valid")
                continue
            else:
                state = get_next_state(state, position)
        elif state[0] == 2:

            new_state, heuristic_value = minimax(state, 3)
            computers_choice = get_computers_choice(state, new_state)
            print("Computer's choice is: ", computers_choice)
            state = new_state

    if state[0] == 2:
        print("You won!")
    else:
        print("Computer won!")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    play()
