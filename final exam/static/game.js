const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status');
const resetBtn = document.getElementById('reset');
const scoreX = document.getElementById('score-x');
const scoreO = document.getElementById('score-o');
const scoreDraw = document.getElementById('score-draw');

let board = Array(9).fill('');
let currentPlayer = 'X';
let gameOver = false;

function updateBoard() {
    document.querySelectorAll('.cell').forEach((cell, idx) => {
        cell.textContent = board[idx];
        cell.className = 'cell';
        if (board[idx] === 'X') cell.classList.add('x');
        if (board[idx] === 'O') cell.classList.add('o');
        cell.disabled = board[idx] !== '' || gameOver || currentPlayer !== 'X';
    });
}

function updateStatus(winner) {
    if (winner === 'X') {
        statusEl.textContent = 'Bravo, vous avez gagné !';
        statusEl.style.color = '#e53935';
    } else if (winner === 'O') {
        statusEl.textContent = "L'IA a gagné !";
        statusEl.style.color = '#388e3c';
    } else if (winner === 'draw') {
        statusEl.textContent = 'Match nul !';
        statusEl.style.color = '#fbc02d';
    } else if (currentPlayer === 'X') {
        statusEl.textContent = 'À vous de jouer !';
        statusEl.style.color = '#e53935';
    } else {
        statusEl.textContent = "Tour de l'IA...";
        statusEl.style.color = '#388e3c';
    }
}

function updateScore(score) {
    scoreX.textContent = score['X'];
    scoreO.textContent = score['O'];
    scoreDraw.textContent = score['draw'];
}

boardEl.addEventListener('click', async (e) => {
    if (!e.target.classList.contains('cell') || gameOver || currentPlayer !== 'X') return;
    const idx = parseInt(e.target.dataset.idx);
    if (board[idx] !== '') return;
    board[idx] = 'X';
    updateBoard();
    updateStatus();
    // Envoyer au backend pour le coup de l'IA
    const res = await fetch('/play', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board, current_player: 'X' })
    });
    const data = await res.json();
    board = data.board;
    updateBoard();
    updateScore(data.score);
    if (data.winner) {
        gameOver = true;
        updateStatus(data.winner);
    } else {
        currentPlayer = 'X';
        updateStatus();
    }
});

resetBtn.addEventListener('click', async () => {
    board = Array(9).fill('');
    currentPlayer = 'X';
    gameOver = false;
    updateBoard();
    updateStatus();
    await fetch('/reset', { method: 'POST' });
    // Recharger le score
    location.reload();
});

// Initialisation
updateBoard();
updateStatus(); 