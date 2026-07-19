import copy


class KnightsTour:
    def __init__(self, n):
        self.N = n
        self.soluzione_completa = None

    def trova_cammino(self, start_x, start_y):
        self.soluzione_completa = None
        # Il cammino parte dalla posizione iniziale scelta
        parziale = [(start_x, start_y)]
        self._ricorsione(parziale)
        return self.soluzione_completa

    def _ricorsione(self, parziale):
        # 1. Controllo di uscita anticipata se abbiamo già finito
        if self.soluzione_completa is not None:
            return

        # 2. Caso terminale
        if len(parziale) == self.N ** 2:
            self.soluzione_completa = copy.deepcopy(parziale)
            return

        # 3. Coordinate attuali del cavallo
        curr_x, curr_y = parziale[-1]
        mosse_possibili = [(2, 1), (1, 2), (-1, -2), (-2, -1), (1, -2), (-2, 1), (-1, 2), (2, -1)]

        # 4. Ciclo sulle mosse
        for mx, my in mosse_possibili:
            next_x = curr_x + mx
            next_y = curr_y + my
            mossa_candidata = (next_x, next_y)

            # Applica i filtri usando il tuo metodo isValid e controllando che non sia già visitata
            if self.isValid(mossa_candidata) and mossa_candidata not in parziale:
                parziale.append(mossa_candidata)
                self._ricorsione(parziale)
                parziale.pop() # Backtracking

    def isValid(self, coords):
        return 0 <= coords[0] < self.N and 0 <= coords[1] < self.N


if __name__ == '__main__':
    # Creiamo un'istanza con una scacchiera 5x5
    dimensione = 5
    solver = KnightsTour(dimensione)

    # Facciamo partire il cavallo dall'angolo in alto a sinistra (0, 0)
    start_x, start_y = 0, 0
    print(f"Calcolo del cammino del cavallo su una scacchiera {dimensione}x{dimensione}...")

    cammino = solver.trova_cammino(start_x, start_y)

    if cammino is not None:
        print("\nCammino trovato con successo!")
        print(f"Numero totale di caselle visitate: {len(cammino)} (Atteso: {dimensione ** 2})")
        print("\nSequenza delle coordinate:")
        print(cammino)

        # Inizializziamo una matrice vuota
        scacchiera = [[0] * dimensione for _ in range(dimensione)]

        # Riempiamo la matrice con il numero della mossa
        for passo, (x, y) in enumerate(cammino):
            scacchiera[x][y] = passo + 1

        print("\nMappa della scacchiera (ordine delle mosse):")
        for riga in scacchiera:
            # Stampiamo i numeri allineati per una lettura ordinata
            print(" ".join(f"{val:2d}" for val in riga))
    else:
        print("\nNessun cammino trovato per questa posizione di partenza.")

