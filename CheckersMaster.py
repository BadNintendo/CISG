class CheckersModule:
    COLOR_RESET = "\033[0m"
    COLOR_GREEN = "\033[92m"
    COLOR_RED = "\033[91m"
    COLOR_CYAN = "\033[96m"
    COLOR_YELLOW = "\033[93m"

    def __init__(self):
        self.data_store = {}
        self.move_counter = 0  # To track the number of non-capture moves
        self.repetitions = {}  # To track board positions for 2-fold repetition
        self.moves_printed = False  # Track if moves have already been printed for this evaluation

    def evaluate_moves(self, board, player_pieces, opponent_pieces):
        if self.moves_printed:  # Avoid re-evaluating or reprinting
            return []

        DIRECTIONS = [-9, -7, 7, 9]  # Possible movement directions
        
        def is_valid_move(pos):
            return 0 <= pos < len(board) and board[pos] is None

        def opponent_threat_analysis(pos, opponent_pieces, board):
            threat_score = 0
            THREAT_DIRECTIONS = [-9, -7, 7, 9]

            for opponent_piece in opponent_pieces:
                for direction in THREAT_DIRECTIONS:
                    adjacent = opponent_piece + direction
                    jump_pos = adjacent + direction

                    if adjacent == pos:
                        threat_score += 5  # Immediate adjacent threat
                    elif 0 <= adjacent < len(board) and board[adjacent] is None and jump_pos == pos:
                        threat_score += 10  # Potential jump threat

            return threat_score

        def championship_moves(moves):
            # Example championship moves logic, pre-defined optimal strategies
            for move in moves:
                if move['type'] == 'move':
                    move['score'] += 2  # Example boost for championship moves
                elif move['type'] == 'jump':
                    move['score'] += 5  # Example boost for jumps in championship moves

        moves = []
        for piece in player_pieces:
            for direction in DIRECTIONS:
                forward_pos = piece + direction

                if is_valid_move(forward_pos):
                    moves.append({"type": "move", "piece": piece, "to": forward_pos, "score": 1})

                attack_pos = piece + direction * 2
                enemy_pos = piece + direction

                if 0 <= enemy_pos < len(board) and board[enemy_pos] == 'enemy' and is_valid_move(attack_pos):
                    risk_score = opponent_threat_analysis(attack_pos, opponent_pieces, board)
                    moves.append({"type": "jump", "piece": piece, "to": attack_pos, "captured": enemy_pos, "score": 10 - risk_score})

        # Consider championship moves or advanced strategies
        championship_moves(moves)

        # Sort moves by score in descending order
        moves = sorted(moves, key=lambda x: x['score'], reverse=True)

        # Select only the top 5 moves from different pieces
        top_moves = []
        selected_pieces = set()
        for move in moves:
            if move['piece'] not in selected_pieces:
                top_moves.append(move)
                selected_pieces.add(move['piece'])
            if len(top_moves) == 5:
                break

        # Print top 5 moves (only once)
        if not self.moves_printed:
            print(self.COLOR_CYAN + "Top 5 Moves:" + self.COLOR_RESET)
            for move in top_moves:
                move_type = "Jump" if move['type'] == "jump" else "Move"
                move_details = f"Piece at {move['piece']} -> {move['to']} ({move_type}, Score: {move['score']})"
                print(self.COLOR_GREEN + move_details + self.COLOR_RESET)
            self.moves_printed = True  # Mark as printed

        return top_moves

    def reset_print_flag(self):
        """Reset the print flag to allow re-evaluation and printing."""
        self.moves_printed = False

    def detect_draw(self, board, player_pieces, opponent_pieces):
        # 50-move rule: Check if 50 moves have passed without a capture, only if one piece is left
        if (len(player_pieces) == 1 or len(opponent_pieces) == 1) and self.move_counter >= 50:
            return True, "50-move rule draw."

        # 2-fold repetition rule: Check if the same board position has occurred twice (only applies if one piece is left)
        if len(player_pieces) == 1 or len(opponent_pieces) == 1:
            board_state = str(board)
            if board_state in self.repetitions:
                self.repetitions[board_state] += 1
                if self.repetitions[board_state] == 2:
                    return True, "2-fold repetition draw."
            else:
                self.repetitions[board_state] = 1

        return False, None

if __name__ == "__main__":
    board = [None] * 64
    player_pieces = [11, 12, 13, 14, 15, 16, 17, 18]  # Player pieces initial positions
    opponent_pieces = [47, 48, 49, 50, 51, 52, 53, 54]  # Opponent pieces initial positions

    checkers = CheckersModule()

    for _ in range(100):  # Simulate moves
        best_moves = checkers.evaluate_moves(board, player_pieces, opponent_pieces)
        is_draw, draw_reason = checkers.detect_draw(board, player_pieces, opponent_pieces)

        if is_draw:
            print(f"{CheckersModule.COLOR_CYAN}{draw_reason}{CheckersModule.COLOR_RESET}")
            break

        # Switch sides (for simplicity, the same evaluation can be applied to opponent)
        ##player_pieces, opponent_pieces = opponent_pieces, player_pieces
        ##board = board[::-1]  # Mirror the board for the opponent's turn
