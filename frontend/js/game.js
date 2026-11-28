
const boardElement = document.getElementById("board");

function createBoard() {
    boardElement.innerHTML = "";

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {

            const square = document.createElement("div");

            square.classList.add("square");

            if ((row + col) % 2 === 0) {
                square.classList.add("light");
            } else {
                square.classList.add("dark");
            }

            // Peças pretas
            if (row < 3 && (row + col) % 2 === 1) {
                const piece = document.createElement("div");
                piece.classList.add("piece", "black-piece");
                square.appendChild(piece);
            }

            // Peças brancas
            if (row > 4 && (row + col) % 2 === 1) {
                const piece = document.createElement("div");
                piece.classList.add("piece", "white-piece");
                square.appendChild(piece);
            }

            boardElement.appendChild(square);
        }
    }
}

document.getElementById("new-game").addEventListener("click", () => {
    createBoard();
});

createBoard();
