/**
 * Evaluates optimal moves for player's pieces, calculating the best forward moves and jumps,
 * considering possible counter-attacks by the opponent.
 * @param {Array} board - 1D array representing the board state, where 'null' indicates empty space,
 *                        'player' indicates player piece, and 'enemy' indicates opponent piece.
 * @param {Array} playerPieces - Array of indices indicating the positions of player pieces on the board.
 * @param {Array} opponentPieces - Array of indices indicating the positions of opponent pieces on the board.
 * @returns {Array} - Array of up to 5 best moves based on scores, sorted from highest to lowest.
 */
const evaluateMoves = (board, playerPieces, opponentPieces) => {
    const DIRECTIONS = [-9, -7, 7, 9]; // Possible movement directions; adjust as needed for board structure.

    /**
     * Checks if a board position is within bounds and empty.
     * @param {number} pos - The index on the board to check.
     * @returns {boolean} - True if the position is valid and empty, otherwise false.
     */
    const isValidMove = (pos) => pos >= 0 && pos < board.length && board[pos] === null;

    // Array of possible moves, flattened for sorting and filtering
    const getTopMoves = playerPieces.flatMap((piece) => {
        let moves = [];
        
        DIRECTIONS.forEach((direction) => {
            const forwardPos = piece + direction;

            // Add a basic forward move if position is empty
            if (isValidMove(forwardPos)) {
                moves.push({ type: 'move', piece, to: forwardPos, score: 1 });
            }

            // Check for potential jumps over enemy pieces
            const attackPos = piece + direction * 2;
            const enemyPos = piece + direction;
            
            if (
                board[enemyPos] === 'enemy' &&
                isValidMove(attackPos) // Ensure the landing position after jump is empty
            ) {
                // Calculate risk level of moving to this position
                const riskScore = opponentThreatAnalysis(attackPos, opponentPieces, board);
                moves.push({ type: 'jump', piece, to: attackPos, captured: enemyPos, score: 10 - riskScore });
            }
        });

        return moves;
    })
    .sort((a, b) => b.score - a.score) // Sort moves by score, highest first
    .slice(0, 5); // Select the top 5 moves based on calculated score

    return getTopMoves;
};

/**
 * Analyzes potential threats posed by the opponent to a given position.
 * @param {number} pos - Position to evaluate for threats by opponent pieces.
 * @param {Array} opponentPieces - Array of indices where opponent pieces are located.
 * @param {Array} board - 1D array representing the board state.
 * @returns {number} - Calculated threat score; higher values indicate greater risk.
 */
const opponentThreatAnalysis = (pos, opponentPieces, board) => {
    let threatScore = 0;
    const THREAT_DIRECTIONS = [-9, -7, 7, 9]; // Possible directions opponent can move/jump

    opponentPieces.forEach((opponentPiece) => {
        THREAT_DIRECTIONS.forEach((direction) => {
            const adjacent = opponentPiece + direction;
            const jumpPos = adjacent + direction;

            // If adjacent to the player's position, assign a threat score
            if (adjacent === pos) {
                threatScore += 5; // Immediate adjacent threat
            } else if (board[adjacent] === 'empty' && jumpPos === pos) {
                threatScore += 10; // Potential jump threat
            }
        });
    });

    return threatScore;
};

// Example board setup
let board = Array(64).fill(null);
let playerPieces = [22, 25, 26]; // Positions of player pieces
let opponentPieces = [31, 33, 36]; // Positions of opponent pieces

// Execute move evaluation
const bestMoves = evaluateMoves(board, playerPieces, opponentPieces);
console.log(bestMoves);
