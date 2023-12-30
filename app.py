# app.py
from flask import Flask, render_template, request, jsonify
import logging  

app = Flask(__name__)

board = [' ' for _ in range(9)]  # Tic Tac Toe board

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    logging.info('Received POST request')
    position = int(request.form.get('position'))
    board[position] = 'X'
    logging.info(f'Player moved: {board}')
    if check_win(board, 'X'):
        return jsonify({'win': True, 'message': 'You win!'})
    ai_move = ai_make_move(board)
    logging.info(f'AI moved: {ai_move}')
    if check_win(board, 'O'):
        return jsonify({'win': True, 'message': 'AI wins!'})
    return jsonify({'win': False, 'board': board})

def check_win(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_conditions)

# Modify the ai_make_move function
def ai_make_move(board):
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i

    if best_move is not None:
        board[best_move] = 'O'

    return best_move

def minimax(board, depth, is_maximizing):
    logging.info(f'minimax called with board {board}, depth {depth}, is_maximizing {is_maximizing}')
    depth_limit = 5  # Define the depth limit

    if check_win(board, 'O'):
        return 1
    elif check_win(board, 'X'):
        return -1
    elif ' ' not in board or depth == depth_limit:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

if __name__ == '__main__':
    app.run(debug=True)
