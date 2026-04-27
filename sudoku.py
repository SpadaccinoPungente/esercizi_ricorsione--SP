
class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid

    def solve(self):
        cell = self.find_empty()
        if not cell: return True  # Risolto!

        row, col = cell
        for num in range(1, 10):
            if self.is_valid_solution(row, col, num):
                self.grid[row][col] = num  # Corretto: uso di self.grid

                if self.solve(): return True

                self.grid[row][col] = 0  # Backtrack (reset)

        return False  # Innesca il ritorno indietro

    def find_empty(self):
        # Scorre la griglia 9x9 per trovare uno 0 (cella vuota).
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def is_valid_solution(self, row, col, num):
        # CONTROLLO RIGA
        # Scorriamo tutte le 9 colonne (j) mantenendo fissa la riga passata come argomento.
        # Se troviamo che 'num' è già lì, la mossa non è valida.
        for j in range(9):
            if self.grid[row][j] == num: return False

        # 2. CONTROLLO COLONNA
        # Scorriamo tutte le 9 righe (i) mantenendo fissa la colonna passata come argomento.
        # Stesso discorso: se troviamo 'num', scartiamo la mossa.
        for i in range(9):
            if self.grid[i][col] == num: return False

        # 3. CONTROLLO SOTTO-QUADRATO 3x3
        # Dobbiamo identificare le coordinate iniziali (angolo in alto a sinistra)
        # del blocco 3x3 in cui si trova la nostra cella attuale (row, col).
        # Usiamo '//' (divisione intera) per ottenere l'indice del blocco (0, 1 o 2)
        # e poi moltiplichiamo per 3 per avere l'indice reale della matrice.
        # Esempio pratico per le righe:
        # Riga 0, 1, 2 -> diviso 3 fa 0 -> per 3 fa 0 (Il blocco inizia a riga 0)
        # Riga 3, 4, 5 -> diviso 3 fa 1 -> per 3 fa 3 (Il blocco inizia a riga 3)
        # Riga 6, 7, 8 -> diviso 3 fa 2 -> per 3 fa 6 (Il blocco inizia a riga 6)
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        # Ora scansioniamo solo il quadrato 3x3 a partire da (start_row, start_col)
        # spostandoci di un massimo di +2 sia in orizzontale che in verticale.
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num: return False

        # Se i tre controlli passano senza far scattare un 'return False',
        # significa che il numero rispetta le regole del Sudoku in quella cella.
        return True

    def print_grid(self):
        for i in range(9):
            # Inserisce un divisore orizzontale ogni 3 righe (escludendo la prima)
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - ")

            for j in range(9):
                # Inserisce un divisore verticale ogni 3 colonne (escludendo la prima)
                if j % 3 == 0 and j != 0:
                    print("| ", end="")

                # Stampa il numero. Se è l'ultimo della riga, va a capo.
                if j == 8:
                    print(self.grid[i][j])
                else:
                    print(str(self.grid[i][j]) + " ", end="")


if __name__ == '__main__':
    # 0 rappresenta le celle vuote
    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    test = SudokuSolver(sudoku)

    print("\nGriglia iniziale:")
    test.print_grid()

    print("\nRisolvendo...\n")

    if test.solve():
        print("Sudoku risolto:")
        test.print_grid()
    else:
        print("Nessuna soluzione trovata.")