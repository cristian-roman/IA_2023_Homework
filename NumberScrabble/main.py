magic_square = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
# player_turn can take value 1 for player 1 or value 2 for player 2
player_turn = 1
square = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
state = (player_turn, square)


def is_final_state(current_player, current_state):
    is_final = False
    for i in range(len(current_state)) and is_final is False:
        if ((current_state[i][0] == current_player and current_state[i][1] == current_player and current_state[i][2]
            == current_player)
                or (current_state[0][i] == current_player and current_state[1][i] ==
                                    current_player and current_state[2][i] == current_player)):
            is_final = True
    if is_final is False:
        if (current_state[0][0] == current_player and current_state[1][1] == current_player and current_state[2][2]
                == current_player) or (current_state[0][2] == current_player and current_state[1][1] ==
                                        current_player and current_state[2][0] == current_player):
            is_final = True
    if is_final is False:
        return False
    else:
        return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
