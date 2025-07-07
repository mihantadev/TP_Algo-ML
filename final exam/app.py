from flask import Flask, render_template, request, jsonify, session
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import os
from flask import redirect, url_for

app = Flask(__name__)
app.secret_key = 'madagascar_secret_key'  # Pour la gestion de session (score)

# Chargement et entraînement du modèle IA
DATA_PATH = 'Tic tac initial results.csv'
data = pd.read_csv(DATA_PATH)
X = data[[f'MOVE{i}' for i in range(1, 8)]].replace('?', -1).astype(int)
y = data['CLASS']
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X, y)

# Fonctions utilitaires pour le jeu
def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for line in wins:
        vals = [board[i] for i in line]
        if vals[0] != '' and vals.count(vals[0]) == 3:
            return vals[0]
    if '' not in board:
        return 'draw'
    return None

def board_to_moves(board, player):
    moves = []
    for i, v in enumerate(board):
        if v == player:
            moves.append(i)
    while len(moves) < 7:
        moves.append(-1)
    return moves

@app.route('/')
def index():
    # Initialisation du score en session
    if 'score' not in session:
        session['score'] = {'X': 0, 'O': 0, 'draw': 0}
    return render_template('index.html', score=session['score'])

@app.route('/reset', methods=['POST'])
def reset():
    session['score'] = {'X': 0, 'O': 0, 'draw': 0}
    return ('', 204)

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    board = data['board']
    current_player = data['current_player']

    # Vérifier si le joueur humain a déjà gagné
    winner = check_winner(board)
    if winner:
        session['score'][winner] += 1 if winner in ['X', 'O'] else 0
        if winner == 'draw':
            session['score']['draw'] += 1
        return jsonify({'board': board, 'winner': winner, 'score': session['score']})

    # 1. Bloquer la victoire du joueur humain si possible
    for i in range(9):
        if board[i] == '':
            temp_board = board.copy()
            temp_board[i] = 'X'
            if check_winner(temp_board) == 'X':
                board[i] = 'O'
                winner = check_winner(board)
                if winner:
                    session['score'][winner] += 1 if winner in ['X', 'O'] else 0
                    if winner == 'draw':
                        session['score']['draw'] += 1
                return jsonify({'board': board, 'winner': winner, 'score': session['score']})

    # 2. Prendre le centre si possible
    if board[4] == '':
        board[4] = 'O'
        winner = check_winner(board)
        if winner:
            session['score'][winner] += 1 if winner in ['X', 'O'] else 0
            if winner == 'draw':
                session['score']['draw'] += 1
        return jsonify({'board': board, 'winner': winner, 'score': session['score']})

    # 3. Sinon, choisir le meilleur coup selon le modèle
    best_score = -1
    best_move = None
    for i in range(9):
        if board[i] == '':
            temp_board = board.copy()
            temp_board[i] = 'O'
            moves = board_to_moves(temp_board, 'O')
            pred = clf.predict([moves])[0]
            score = {'win':2, 'draw':1, 'loss':0}[pred]
            if score > best_score:
                best_score = score
                best_move = i
    if best_move is not None:
        board[best_move] = 'O'

    winner = check_winner(board)
    if winner:
        session['score'][winner] += 1 if winner in ['X', 'O'] else 0
        if winner == 'draw':
            session['score']['draw'] += 1
    return jsonify({'board': board, 'winner': winner, 'score': session['score']})

if __name__ == '__main__':
    app.run(debug=True) 