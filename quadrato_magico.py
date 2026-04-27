import copy
from time import time


class QuadratoMagico():
    def __init__(self, N):
        self.N = N
        self.n_chiamate = 0
        self.n_soluzioni = 0
        self.soluzioni = []

    # [Prof] Soluzione del quadrato magico rappresentata da un vettore di N**2 elementi,
    # ogni elemento rappresenta una cella del quadrato, e il suo valore è il numero che
    # mettiamo nella cella.
    def risolvi_quadrato(self):
        self.n_chiamate = 0
        self.n_soluzioni = 0
        self.soluzioni = []
        # [Gemini] Passo iniziale: la lista parziale è vuota, l'insieme dei numeri disponibili
        # contiene tutti i numeri da 1 a N^2. Usare un set garantisce verifiche veloci
        # ed evita di pescare duplicati.
        self._ricorsione([], set(range(1, self.N * self.N + 1)))

    def _ricorsione(self, parziale, rimanenti):
        self.n_chiamate += 1

        # [Prof] caso terminale
        # [Gemini] Base case della ricorsione: se ho riempito tutte le N*N celle,
        # ho una potenziale soluzione completa.
        if len(parziale) == self.N * self.N:
            # [Gemini] Verifica definitiva includendo le diagonali (non controllate prima).
            if self._is_valid(parziale):
                self.n_soluzioni += 1
                # [Gemini] Devo fare una copia di 'parziale'. Se facessi solo append(parziale),
                # appenderei un riferimento alla lista che poi, a causa del backtracking,
                # verrebbe svuotata portando a un risultato finale di liste vuote.
                # N.B. copy.deepcopy è eccessivo qui, basterebbe append(list(parziale)).
                self.soluzioni.append(copy.deepcopy(parziale))
            # print(parziale)

        # [Prof] caso ricorsivo
        else:
            for numero in rimanenti:
                # [Prof] 0) fare controllo dei vincoli
                # [Prof] 1) aggiungere numero a parziale
                # [Gemini] Fase di "Scelta": provo a mettere 'numero' nella prossima cella libera.
                parziale.append(numero)

                # [Gemini] Pruning (Potatura): controllo se la mossa appena fatta ha reso
                # il quadrato già invalido. Se sì, è inutile continuare a scendere nell'albero.
                if self._is_parziale_valid(parziale):
                    # [Prof] 1b) tolgo il numero appena inserito dai rimanenti
                    # [Gemini] ATTENZIONE: deepcopy su un set di interi è lentissimo.
                    # Molto più efficiente scrivere: nuovi_rimanenti = rimanenti - {numero}
                    nuovi_rimanenti = copy.deepcopy(rimanenti)
                    nuovi_rimanenti.remove(numero)

                    # [Prof] 2) andare avanti nella ricorsione
                    # [Gemini] Esploro le configurazioni future nate da questa scelta.
                    self._ricorsione(parziale, nuovi_rimanenti)

                # [Prof] 3) backtracking
                # [Gemini] Fase di "Annullamento": la via esplorata in profondità ha fallito,
                # oppure ha trovato la soluzione e ha concluso. Tolgo l'ultimo numero
                # inserito per liberare la cella e provare il prossimo numero del ciclo 'for'.
                parziale.pop()

    def _is_parziale_valid(self, parziale):
        # [Gemini] Costante magica calcolata in base a N
        numero_magico = self.N * (self.N * self.N + 1) / 2

        # [Prof] 1) controllare righe
        # [Gemini] Calcolo quante righe intere sono già state riempite.
        n_righe_completate = len(parziale) // self.N
        for id_riga in range(n_righe_completate):
            # [Gemini] Tramite lo slicing prendo chunk di N elementi che rappresentano la riga
            riga = parziale[id_riga * self.N:(id_riga + 1) * self.N]
            if sum(riga) != numero_magico:
                return False

        # [Prof] 2) controllare le colonne
        # [Gemini] Una colonna si dice completata solo quando la lista 'parziale' ha
        # raggiunto o superato l'ultima riga di quella specifica colonna.
        n_col_completate = max(len(parziale) - self.N * (self.N - 1), 0)
        for id_col in range(n_col_completate):
            # [Gemini] Slicing "saltellante": parte dalla colonna, finisce alla fine della griglia,
            # e salta di N in N per prendere proprio gli elementi in verticale.
            col = parziale[id_col: (self.N - 1) * self.N + id_col + 1: self.N]
            if sum(col) != numero_magico:
                return False

        # [Prof] #3) controllare diagonale 1
        # [Prof] # diagonale1 = potenziale_soluzione[0:self.N**2+1:self.N+1]
        # [Prof] # if sum(diagonale1) != numero_magico:
        # [Prof] #     return False
        # [Prof] #4) controllare diagonale 2
        # [Prof] # somma = 0
        # [Prof] # for indice in range(self.N):
        # [Prof] #     somma += potenziale_soluzione[indice*self.N + (self.N-1 - indice)]
        # [Prof] # if somma != numero_magico:
        # [Prof] #     return False
        # [Gemini] Il professore le ha commentate qui perché le diagonali non si possono
        # valutare completamente finché non inseriamo gli ultimi elementi in fondo alla griglia.

        # [Prof] 5) passati tutti i controlli, possiamo ritornare True
        return True

    def _is_valid(self, potenziale_soluzione):
        # [Gemini] A differenza di is_parziale_valid, qui sappiamo che l'array è pieno (lunghezza N*N).
        numero_magico = self.N * (self.N * self.N + 1) / 2

        # [Prof] 1) controllare righe
        for id_riga in range(self.N):
            riga = potenziale_soluzione[id_riga * self.N:(id_riga + 1) * self.N]
            if sum(riga) != numero_magico:
                return False

        # [Prof] 2) controllare le colonne
        for id_col in range(self.N):
            col = potenziale_soluzione[id_col: (self.N - 1) * self.N + id_col + 1: self.N]
            if sum(col) != numero_magico:
                return False

        # [Prof] 3) controllare diagonale 1
        # [Gemini] Lo step N+1 estrae la diagonale principale (es in 3x3 prende indici 0, 4, 8)
        diagonale1 = potenziale_soluzione[0:self.N ** 2 + 1:self.N + 1]
        if sum(diagonale1) != numero_magico:
            return False

        # [Prof] 4) controllare diagonale 2
        # [Gemini] La logica per la diagonale secondaria prende gli indici da alto-dx a basso-sx
        # (es in 3x3 prende indici 2, 4, 6)
        somma = 0
        for indice in range(self.N):
            somma += potenziale_soluzione[indice * self.N + (self.N - 1 - indice)]
        if somma != numero_magico:
            return False

        # [Prof] 5) passati tutti i controlli, possiamo ritornare True
        return True

    def stampa_quadrato(self, soluzione):
        print("-------------")
        for riga in range(self.N):
            print(soluzione[riga * self.N: (riga + 1) * self.N])
        print("-------------")


if __name__ == '__main__':
    qm = QuadratoMagico(3)
    start_time = time()
    qm.risolvi_quadrato()
    end_time = time()

    print(f"Tempo impiegato = {end_time - start_time}")
    print(f"Chiamate effettuate = {qm.n_chiamate}")
    print(f"Soluzioni trovate = {qm.n_soluzioni}")
    for soluzione in qm.soluzioni:
        qm.stampa_quadrato(soluzione)