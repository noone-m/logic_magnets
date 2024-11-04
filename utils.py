from math import floor

def handle_click(board, pos, selected_token):
    """
    Handles a click to either select a token or move it to a new position.
    """
    # Convert screen coordinates to board coordinates
    col = min(board.width - 1, max(0, round((pos[0]) / (800 / (board.width + 1)) - 1)))
    row = min(board.height - 1, max(0, round((pos[1]) / (600 / (board.height + 1)) - 1)))
    if selected_token['value'] is None:
        # First click: Attempt to select a token
        if (row, col) in board.tokens and board.tokens[(row, col)] in {'R', 'P'}:
            selected_token['value'] = (row, col)
    else:
        # Second click: Attempt to move the selected token
        if board.board[row][col] == 'E':  # Ensure the target cell is empty
            old_row, old_col = selected_token['value']
            token_type = board.tokens.pop((old_row, old_col))  # Remove from the old position
            board.board[old_row][old_col] = 'E'  # Clear old cell

            # Move to new position
            board.board[row][col] = token_type
            board.tokens[(row, col)] = token_type
            selected_token['value'] = None  
            board.apply_logic({(row,col):token_type})
        else:
            # If the target position is invalid, deselect without moving
            selected_token['value'] = None  
    print(f'selected : {selected_token}')


def get_four_sides_cells(board,row,col):
    up_cells = []
    down_cells = []
    left_cells = []
    right_cells = []
    for i in range(board.height):
        if i < row:
            up_cells.append({(i,col):board.board[i][col]})
        if i> row:
            down_cells.append({(i,col):board.board[i][col]})
    for i in range(board.width):
        if i < col:
            left_cells.append({(row,i):board.board[row][i]})
        if i> col:
            right_cells.append({(row,i):board.board[row][i]})
    up_cells = list(reversed(up_cells))
    left_cells = list(reversed(left_cells))
    print(up_cells)
    print(down_cells)
    print(left_cells)
    print(right_cells)
    return up_cells,down_cells,left_cells,right_cells


def pull_down(board, up_cells):
    if up_cells:
        first_value = list(up_cells[0].values())[0]
        if first_value != 'E':
            return
        else:
            for dic in up_cells:
                for (row,col),value in dic.items():
                    if value in ['R','P','B']:
                        board.board[row][col] = 'E'
                        board.board[row+1][col] = value
                        board.tokens.pop((row,col))
                        board.tokens[(row+1,col)] = value
                        return 
                    elif value == 'D':
                        return

def pull_up(board, down_cells):
    if down_cells:
        first_value = list(down_cells[0].values())[0]
        if first_value != 'E':
            return
        else:
            for dic in down_cells:
                for (row,col),value in dic.items():
                    if value in ['R','P','B']:
                        board.board[row][col] = 'E'
                        board.board[row-1][col] = value
                        board.tokens.pop((row,col))
                        board.tokens[(row-1,col)] = value
                        return
                    elif value == 'D':
                        return

def pull_right(board, left_cells):
    if left_cells:
        first_value = list(left_cells[0].values())[0]
        if first_value != 'E':
            return
        else:
            for dic in left_cells:
                for (row,col),value in dic.items():
                    if value in ['R','P','B']:
                        board.board[row][col] = 'E'
                        board.board[row][col+1] = value
                        board.tokens.pop((row,col))
                        board.tokens[(row,col+1)] = value
                        return
                    elif value == 'D':
                        return

def pull_left(board, right_cells):
    if right_cells:
        first_value = list(right_cells[0].values())[0]
        if first_value != 'E':
            return
        else:
            for dic in right_cells:
                for (row,col),value in dic.items():
                    if value in ['R','P','B']:
                        board.board[row][col] = 'E'
                        board.board[row][col-1] = value
                        board.tokens.pop((row,col))
                        board.tokens[(row,col-1)] = value
                        return
                    elif value == 'D':
                        return
def is_pushed(cells):
    for dic in cells:
        for value in dic.values():
            if value == 'D':
                return False
            if value == 'E':
                return True
    return False
    
def pushed_cells(cells):
    pushed_cells = []
    for dic in cells:
        for key,value in dic.items():
            if value == 'E':
                return pushed_cells
            if value in ['R','P','B']:
                pushed_cells.append({key:value})

def push_down(board, down_cells):
    if down_cells:
        for dic in down_cells:
            for (row,col),value in dic.items():
                if value in ['R','P','B']:
                    _,down_cells2,_,_ = get_four_sides_cells(board, row, col)
                    if is_pushed(down_cells2):
                        push_down(board,down_cells2)
                    else:
                        return
                    if 0<= row + 1 < board.height:
                        board.board[row][col] = 'E'
                        board.board[row+1][col] = value   
                        board.tokens.pop((row,col))
                elif value == 'D':
                    return

def push_up(board, up_cells):
    if up_cells:
        for dic in up_cells:
            for (row,col),value in dic.items():
                if value in ['R','P','B']:
                    up_cells2,_,_,_ = get_four_sides_cells(board, row, col)
                    if is_pushed(up_cells2):
                        push_up(board,up_cells2)
                    else:
                        return
                    if 0<= row - 1 < board.height:
                        board.board[row][col] = 'E'
                        board.board[row-1][col] = value   
                        board.tokens.pop((row,col))
                        board.tokens[(row-1,col)] = value
                elif value == 'D':
                    return


def push_right(board, right_cells):
    if right_cells:
        for dic in right_cells:
            for (row,col),value in dic.items():
                if value in ['R','P','B']:
                    _,_,_,right_cells2 = get_four_sides_cells(board, row, col)
                    if is_pushed(right_cells2):
                        push_right(board,right_cells2)
                    else:
                        return
                    if 0<= col + 1 < board.width:
                        board.board[row][col] = 'E'
                        board.board[row][col+1] = value   
                        board.tokens.pop((row,col))
                        board.tokens[(row,col+1)] = value

                elif value == 'D':
                    return



def push_left(board, left_cells):
    if left_cells:
        for dic in left_cells:
            for (row,col),value in dic.items():
                if value in ['R','P','B']:
                    _,_,left_cells2,_ = get_four_sides_cells(board, row, col)
                    if is_pushed(left_cells2):
                        pull_left(board,left_cells2)
                    else:
                        return
                    if 0<= col - 1 < board.width:
                        board.board[row][col] = 'E'
                        board.board[row][col-1] = value   
                        board.tokens.pop((row,col))
                        board.tokens[(row,col-1)] = value

                    return
                elif value == 'D':
                    return
