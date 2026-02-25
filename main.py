"""Main entry point for the Hex game."""

import time
from board import HexBoard
from player import HumanPlayer
from ai_easy import EasyAI
from ai_medium import MediumAI
from ai_hard import HardAI
from utils import RED, BLUE, PLAYER_NAMES, format_move

DEFAULT_SIZE = 11

AI_CLASSES = {
    '1': ('Easy', EasyAI),
    '2': ('Medium', MediumAI),
    '3': ('Hard', HardAI),
}


def play_game(player1, player2, board, display=True):
    """Run a game between two players.

    player1 plays RED, player2 plays BLUE.
    Returns the winning player's color (RED or BLUE), or None if quit.
    """
    players = {RED: player1, BLUE: player2}
    current_color = RED
    move_count = 0

    if display:
        print(f"\n{'='*50}")
        print(f"  {player1} (Red)  vs  {player2} (Blue)")
        print(f"{'='*50}")
        board.display()

    while True:
        current_player = players[current_color]

        if display:
            print(f"\n--- {current_player}'s turn ---")

        start = time.time()
        move = current_player.get_move(board)
        elapsed = time.time() - start

        if move is None:
            if display:
                print("\nGame quit.")
            return None

        r, c = move
        board.place(r, c, current_color)
        move_count += 1

        if display:
            print(f"  {current_player} plays {format_move(r, c)}  ({elapsed:.2f}s)")
            board.display()

        if board.check_win(current_color):
            if display:
                print(f"\n{'*'*50}")
                print(f"  {current_player} wins in {move_count} moves!")
                print(f"{'*'*50}")
            return current_color

        current_color = RED if current_color == BLUE else BLUE


def choose_ai_level(prompt):
    """Prompt user to select an AI difficulty level."""
    while True:
        print(f"\n{prompt}")
        print("  1) Easy")
        print("  2) Medium")
        print("  3) Hard")
        choice = input("  Choice: ").strip()
        if choice in AI_CLASSES:
            return choice
        print("  Invalid choice. Enter 1, 2, or 3.")


def human_vs_ai():
    """Set up and play a Human vs AI game."""
    # Choose color
    while True:
        print("\nChoose your color:")
        print("  1) Red (connect top <-> bottom, plays first)")
        print("  2) Blue (connect left <-> right, plays second)")
        choice = input("  Choice: ").strip()
        if choice in ('1', '2'):
            break
        print("  Invalid choice.")

    human_color = RED if choice == '1' else BLUE
    ai_color = BLUE if human_color == RED else RED

    # Choose AI level
    level_key = choose_ai_level("Select AI difficulty:")
    level_name, ai_class = AI_CLASSES[level_key]

    # Choose board size
    size = input(f"\nBoard size (default {DEFAULT_SIZE}): ").strip()
    size = int(size) if size.isdigit() and 2 <= int(size) <= 19 else DEFAULT_SIZE

    board = HexBoard(size)
    human = HumanPlayer(human_color)
    ai = ai_class(ai_color)

    if human_color == RED:
        play_game(human, ai, board)
    else:
        play_game(ai, human, board)


def ai_vs_ai_watch():
    """Set up and watch an AI vs AI game."""
    level1_key = choose_ai_level("Select RED AI (top <-> bottom):")
    level2_key = choose_ai_level("Select BLUE AI (left <-> right):")

    _, ai1_class = AI_CLASSES[level1_key]
    _, ai2_class = AI_CLASSES[level2_key]

    size = input(f"\nBoard size (default {DEFAULT_SIZE}): ").strip()
    size = int(size) if size.isdigit() and 2 <= int(size) <= 19 else DEFAULT_SIZE

    board = HexBoard(size)
    player1 = ai1_class(RED)
    player2 = ai2_class(BLUE)

    play_game(player1, player2, board, display=True)


def main_menu():
    """Display the main menu and handle user selection."""
    print("\n" + "=" * 50)
    print("         H E X   G A M E")
    print("=" * 50)

    while True:
        print("\nMain Menu:")
        print("  1) Human vs AI")
        print("  2) AI vs AI (watch)")
        print("  3) Tournament")
        print("  4) Quit")
        choice = input("  Choice: ").strip()

        if choice == '1':
            human_vs_ai()
        elif choice == '2':
            ai_vs_ai_watch()
        elif choice == '3':
            from tournament import run_tournament_menu
            run_tournament_menu()
        elif choice == '4':
            print("\nGoodbye!")
            break
        else:
            print("  Invalid choice. Enter 1-4.")


if __name__ == '__main__':
    main_menu()
