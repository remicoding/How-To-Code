def create_board():
    """Returns a list of zeros representing an empty sudoku baord"""
    return [i * 0 for i in range(1, 82)]


def print_board(board):
    """
    Creates a format and prints the board as a 9x9 sudoku table

    Argument:
    'board': list representing a sudoku board
    """
    for i in range(81):
        if i == 0:
            print("  0   1   2    3   4   5    6   7   8")
            print("-" * 39)
        row_format = "| {} ".format(board[i])
        if i > 0 and (i + 1) % 3 == 0 and (i + 1) % 9 != 0:
            row_format = row_format + "|"
        print(row_format, end="")
        if (i + 1) % 9 == 0:
            print("|\n" + "-" * 39)
        if (i + 1) % 27 == 0 and (i + 1) != 81:
            print("-" * 39)


def get_position(row, col):
    """
    Returns the index of the value corresponding to the row and col
    
    Arguments:
    'row': row on a 9x9 sudoku board
    'col': column on a 9x9 sudoku board
    """
    return (row * 9) + col


def get_row_col(position):
    """
    Returns the row and column of the position on a 9x9 sudoku board

    Argument:
    'position': index of the value in the list that represents the board
    """
    return position // 9, position % 9


def rows():
    """
    Generates all the possible row wise index on the sudoku board
    
    Example:
    [[0, 1, 2, ...],
     [9, 10, 11, ...]]
    """
    return [[(9 * i) + j for j in range(9)] for i in range(9)]


def cols():
    """
    Generates all the possible column wise index on the sudoku board
    
    Example:
    [[0, 9, 18, ...],
     [1, 10, 19, ...]]
    """
    return [[(9 * j) + i for j in range(9)] for i in range(9)]


def boxes():
    """
    Generates all the possible box wise index on the sudoku board

    Boxes represent the 3x3 area on the sudoku board that needs to be filled
    will a value [1, 9] and which sudoku rules apply

    Example:
    [[0, 1, 2, [9, 10, 11,
      3, 4, 5,  12, 13, 14,
      6, 7, 8], 15, 16, 17], ...]
    """
    list_out = []
    for i in range(9):
        if i % 3 == 0:
            row_0 = [i * 9, i * 9]
        else:
            row_0[0] += 3
            row_0[1] += 3
        row = []
        for j in range(9):
            if j > 0 and j % 3 == 0:
                row.append(row_0[0] + j * 3)
                row_0[1] = row_0[0] + j * 3
            else:
                row.append(row_0[1] + j % 3)
        list_out.append(row)
        row_0[1] = row_0[0]
    return list_out


def units():
    """
    Generates all the possible row, column, and box wise index on the sudoku board
    in a list of list. 
    """
    one_row = rows()
    one_col = cols()
    one_box = boxes()
    one_row.extend(one_col)
    one_row.extend(one_box)
    return one_row.copy()


def read_square(board, position):
    """
    Returns the value at the specified position on the board

    Arguments:
    'board': list representing a sudoku board
    'position': index of the value desired on the board
    """
    return board[position]


def fill_board(val, board, row=None, col=None):
    """
    Insert the value into the board at the specified row or column

    Arguments:
    'val': value (int) to be entered into the board
    'board': list representing a sudoku board
    'row': row on a 9x9 sudoku board
    'col': column on a 9x9 sudoku board
    """
    board_out = board.copy()
    if row == None:
        for i in range(9):
            board_out[get_position(i, col)] = val[i]
    elif col == None:
        board_out[get_position(row, 0):get_position(row, 0) + 8] = val
    else:
        board_out[get_position(row, col)] = val
    return board_out


def solve_sudoku(board):
    """
    Solved the sudoku board

    Argument:
    'board': list representing a sudoku board
    """

    # arbitrary-arity tree function
    def solve_board(board):
        """
        Helper function: solves a single sudoku board a time

        Argument:
        'board': list representing a sudoku board
        """
        # generative recursion
        if solved(board):
            return board
        return solve_list_board(next_boards(board))

    def solve_list_board(list_board):
        """
        Helper function: makes sure that sudoku board generated in a list are solved

        Argument:
        'board': list representing a sudoku board
        """
        if not list_board:
            return False
        else:
            # backtracking search
            result = solve_board(list_board[0])
            if result is not False:
                return result
            else:
                return solve_list_board(list_board[1:])

    # trampoline
    return solve_board(board)


def solved(board):
    """
    Check if a board is solved, returning True or False

    Argument:
    'board': list representing a sudoku board
    """
    return all(board)


def next_boards(board):
    """
    Generates the next board to be solved

    Argument:
    'board': list representing a sudoku board
    """
    return keep_valid(fill_1_9(find_blank(board), board))


def find_blank(board):
    """
    Returns the index of the next blind spot on the board

    Argument:
    'board': list representing a sudoku board
    """
    if not board:
        print("The board didn't have a blank space.")
    else:
        if not board[0]:
            return 0
        else:
            # self reference - recursion
            return find_blank(board[1:]) + 1


def fill_1_9(position, board):
    """
    Generates a list of 9 boards by replacing the blank spot in the given board with
    values from 1 to 9

    Arguments:
    'position': index of the value desired on the board
    'board': list representing a sudoku board
    """
    position_row, position_col = get_row_col(position)
    return [
        fill_board(i, board, position_row, position_col) for i in range(1, 10)
    ]


def keep_valid(list_boards):
    """
    Returns a list of boards that are valid according to the rules of the sudoku game

    Argument:
    'board': list representing a sudoku board
    """
    return list(filter(valid_board, list_boards))


def valid_board(board):
    """
    Checks to guarantee that a board is valid according to the rules of sudoku

    Argument:
    'board': list representing a sudoku board
    """

    def valid_units(list_unit):
        return all(map(valid_unit, list_unit))

    def valid_unit(unit):
        return no_duplicate(keep_values(read_unit(unit)))

    def read_unit(unit):
        return list(map(read_position, unit))

    def read_position(position):
        return read_square(board, position)

    def keep_values(list_number):
        return [val for val in list_number if val]

    def no_duplicate(list_value):
        if not list_value:
            return True
        else:
            if list_value[0] in list_value[1:]:
                return False
            else:
                return no_duplicate(list_value[1:])

    return valid_units(units())


# Program run setup
def main():
    # Example board to solve
    BD4 = [
        2,
        7,
        4,
        0,
        9,
        1,
        0,
        0,
        5,
        1,
        0,
        0,
        5,
        0,
        0,
        0,
        9,
        0,
        6,
        0,
        0,
        0,
        0,
        3,
        2,
        8,
        0,
        0,
        0,
        1,
        9,
        0,
        0,
        0,
        0,
        8,
        0,
        0,
        5,
        1,
        0,
        0,
        6,
        0,
        0,
        7,
        0,
        0,
        0,
        8,
        0,
        0,
        0,
        3,
        4,
        0,
        2,
        0,
        0,
        0,
        0,
        0,
        9,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        7,
        0,
        8,
        0,
        0,
        3,
        4,
        9,
        0,
        0,
        0,
    ]

    # solution to the board to compare
    BD4s = [
        2,
        7,
        4,
        8,
        9,
        1,
        3,
        6,
        5,
        1,
        3,
        8,
        5,
        2,
        6,
        4,
        9,
        7,
        6,
        5,
        9,
        4,
        7,
        3,
        2,
        8,
        1,
        3,
        2,
        1,
        9,
        6,
        4,
        7,
        5,
        8,
        9,
        8,
        5,
        1,
        3,
        7,
        6,
        4,
        2,
        7,
        4,
        6,
        2,
        8,
        5,
        9,
        1,
        3,
        4,
        6,
        2,
        7,
        5,
        8,
        1,
        3,
        9,
        5,
        9,
        3,
        6,
        1,
        2,
        8,
        7,
        4,
        8,
        1,
        7,
        3,
        4,
        9,
        5,
        2,
        6,
    ]

    # printing the board before and after it is solved
    print_board(BD4)
    print()
    print_board(solve_sudoku(BD4s))


if __name__ == "__main__":
    main()
