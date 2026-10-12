import csv
from operator import attrgetter
from strumento import Strumento #importo le classi create dagli altri file per poter risolvere le richieste
from prestito import Prestito #le creo in un altro file per poter lavorare su di esse piu liberamente

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome=nome
        self.__responsabile=responsabile
        self.strumenti=[] #creo una collezione di oggetti all'interno di una classe
        self.prestiti=[] #creo lista per iterare sui prestiti

    @property
    def responsabile(self):
        return self.__responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        if nuovo_responsabile.strip()=="": #mi assicuro che il nome del nuovo responsabile sia corretto
            raise ValueError("Responsabile incorretto")
        self.__responsabile=nuovo_responsabile


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, "r", encoding="utf_8") as f:
                reader=csv.DictReader(f,fieldnames=["id_strumento","tipo","marca","anno_acquisto","valore"])
                for s in reader:
                    strumento=Strumento(s["id_strumento"],s["tipo"],s["marca"],s["anno_acquisto"],s["valore"])
                    self.strumenti.append(strumento)
        except FileNotFoundError: #nel caso in cui il file non esista
            raise FileNotFoundError #sollevo un'eccezione

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        id_strumento="S"+str(len(self.strumenti)+1) #faccio in modo che lo strumento sia numerato correttamente
        strumento=Strumento(id_strumento, tipo, marca, anno_acquisto, valore) #creo l'oggetto strumento
        self.strumenti.append(strumento) #aggiungo l'oggetto alla collezione di oggetti
        return strumento


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        strumenti_ordinati=self.strumenti.copy() #creo una copia della lista cosi da poterla ordinare senza modificare l'originale
        strumenti_ordinati.sort(key=attrgetter("marca")) #uso operator per ordinarli
        return strumenti_ordinati


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        #controllo che il prestito sia possibile
        presente=False #variabile booleana
        for strumento in self.strumenti:
            if strumento.id_strumento==id_strumento: #se gli l'ID richiesto è presente nel file, continuo
                presente=True

        if presente==False: #altrimenti, sollevo un'eccezione
            raise Exception ("Strumento non esistente")

        for prestito in self.prestiti: #controllo che lo strumento sia disponibile
            if prestito.id_strumento==id_strumento:
                raise Exception ("Strumento richiesto già in prestito")

        if self.prestiti:  # numero i prestiti
            # ricavo i numeri degli ID di tutti i prestiti presenti nella lista
            numeri = [int(prestito.id_prestito[1:]) for prestito in self.prestiti]
            id_prestito = "P" + str(
                max(numeri) + 1)  # trovo l'ID piu grande e aggiungo uno per assegnare l'ID al nuovo prestito
        else:
            id_prestito = "P1"  # altrimenti, se non ci sono ancora prestiti gli assegno P1

        prestito=Prestito(id_prestito,data,id_strumento,cognome_allievo) #creo l'oggetto prestito
        self.prestiti.append(prestito) #lo aggiungo alla lista dei prestiti
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        for prestito in self.prestiti:
            if prestito.id_prestito==id_prestito:
                self.prestiti.remove(prestito) #con il comando remove elimino l'oggetto dalla lista
                break #non continua a cercare se trova una corrispondenza nei prestiti
            else:
                raise Exception #sollevo un'eccezione generica nel caso in cui l'id non sia presente
