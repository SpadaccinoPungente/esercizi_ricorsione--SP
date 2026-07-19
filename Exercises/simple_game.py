import copy


class MonsterGame:
    def __init__(self, matrice):
        self.griglia = matrice
        self.target = 50
        self._best_path = []

    def gioca(self, start_row, start_col):
        self._best_path = []
        parziale = [(start_row, start_col)]
        self._ricorsione(parziale)
        return self._best_path

    def _ricorsione(self, parziale):
        if len(self._best_path) > 0:
            return

        if self.getScore(parziale) > self.target:
            return

        if self.getScore(parziale) == self.target:
            self._best_path = copy.deepcopy(parziale)
            return

        curr_x, curr_y = parziale[-1]
        mosse_possibili = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for mx, my in mosse_possibili:
            next_x = curr_x + mx
            next_y = curr_y + my
            mossa_candidata = (next_x, next_y)

            if self.isValid(mossa_candidata) and mossa_candidata not in parziale:
                parziale.append(mossa_candidata)
                self._ricorsione(parziale)
                parziale.pop()

    def getScore(self, parziale):
        return sum(self.griglia[i][j] for (i, j) in parziale)

    def isValid(self, coords):
        return 0 <= coords[0] < len(self.griglia) and 0 <= coords[1] < len(self.griglia[0])

if "__main__" == __name__:
    if __name__ == "__main__":
        # Creiamo una griglia di esempio basata sui numeri sparsi della slide
        matrice_esempio = [
            [5, 6, 7, 3],
            [9, 1, 2, 4],
            [1, 9, 2, 3],
            [8, 2, 3, 5]
        ]

        gioco = MonsterGame(matrice_esempio)

        # Proviamo a partire dalla cella (0, 0) che contiene il valore 5
        print("Ricerca di un cammino per raggiungere esattamente il punteggio 50...")
        cammino_vincente = gioco.gioca(0, 0)

        if cammino_vincente:
            print("\nHai battuto il mostro! Cammino trovato:")
            print(cammino_vincente)

            # Stampiamo i valori reali delle celle visitate per fare una contro-verifica
            valori_celle = [matrice_esempio[r][c] for (r, c) in cammino_vincente]
            print(f"Valori delle caselle toccate: {valori_celle}")
            print(f"Somma totale: {sum(valori_celle)} (Atteso: 50)")
        else:
            print("\nNessun cammino valido trovato a partire da questa posizione.")