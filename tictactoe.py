from colorama import Fore, Style, init
init(autoreset=True)
def print_board(board):
    """Display the current state of the game board with colors."""
    symbol_map = {
        'X': Fore.CYAN + 'X' + Style.RESET_ALL,
        'O': Fore.YELLOW + 'O' + Style.RESET_ALL,
        ' ': ' '
    }
    print("\n" + "=" * 30)
    for i in range(0, 9, 3):
        row = f" {symbol_map[board[i]]} | {symbol_map[board[i+1]]} | {symbol_map[board[i+2]]} "
        print(row)
        if i < 6:
            print("---+---+---")
    print("=" * 30 + "\n")
def check_winner(board, player):
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],[0, 3, 6], 
        [1, 4, 7],[2, 5, 8],[0, 4, 8], [2, 4, 6]]
    return any(all(board[i] == player for i in pattern) for pattern in win_patterns)
def is_board_full(board):
    return all(cell != ' ' for cell in board)
def get_empty_cells(board):
    return [i for i, cell in enumerate(board) if cell == ' ']
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, 'O'):
        return 10 - depth
    if check_winner(board, 'X'):
        return depth - 10
    if is_board_full(board):
        return 0
    if is_maximizing:
        best_score = -float('inf')
        for i in get_empty_cells(board):
            board[i] = 'O'
            score = minimax(board, depth + 1, False, alpha, beta)
            board[i] = ' '
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for i in get_empty_cells(board):
            board[i] = 'X'
            score = minimax(board, depth + 1, True, alpha, beta)
            board[i] = ' '
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score
def ai_move(board):
    best_score = -float('inf')
    best_move = None
    for i in get_empty_cells(board):
        board[i] = 'O'
        score = minimax(board, 0, False, -float('inf'), float('inf'))
        board[i] = ' '
        if score > best_score:
            best_score = score
            best_move = i
    return best_move
def display_intro():
    print(Fore.GREEN + "\nWelcome to Tic-Tac-Toe!")
    print("You play as 'X' and the AI plays as 'O'.")
    print("Choose a position using this layout:")
    print(Fore.BLUE + " 0 | 1 | 2")
    print("---+---+---")
    print(" 3 | 4 | 5")
    print("---+---+---")
    print(" 6 | 7 | 8\n" + Style.RESET_ALL)
def display_move_history(history):
    print(Fore.MAGENTA + "\nGame Move History:")
    for turn, pos in history:
        print(f"{turn} moved to position {pos}")
    print(Style.RESET_ALL)
def main():
    board = [' ' for _ in range(9)]
    current_player = 'X'
    moves_history = []
    display_intro()
    while True:
        print_board(board)
        if current_player == 'X':
            try:
                move = int(input(Fore.CYAN + "Your move (0-8): " + Style.RESET_ALL))
                if move < 0 or move > 8 or board[move] != ' ':
                    print(Fore.RED + "Invalid move! Please try again.\n")
                    continue
            except ValueError:
                print(Fore.RED + "Invalid input! Enter a number between 0 and 8.\n")
                continue
            board[move] = 'X'
            moves_history.append(("You", move))
        else:
            print(Fore.YELLOW + "AI is making a move..." + Style.RESET_ALL)
            move = ai_move(board)
            board[move] = 'O'
            moves_history.append(("AI", move))
        if check_winner(board, current_player):
            print_board(board)
            print(Fore.GREEN + f"\n{'Congratulations! You' if current_player == 'X' else 'AI'} won the game!")
            display_move_history(moves_history)
            break
        if is_board_full(board):
            print_board(board)
            print(Fore.CYAN + "\nIt's a draw!")
            display_move_history(moves_history)
            break
        current_player = 'O' if current_player == 'X' else 'X'
if __name__ == "__main__":
    main()