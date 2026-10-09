import csv
from operator import attrgetter
class Strumento: #creo una nuova classe,strumento
    def __init__(self,id_strumento,tipo,marca,anno_acquisto,valore):
        self.id_strumento=id_strumento
        self.tipo=tipo
        self.marca=marca
        self.anno_acquisto=anno_acquisto
        self.valore=valore

    def __str__(self): #funzione __str__ per poterlo stampare
        return f"{self.id_strumento},{self.tipo},{self.marca},{self.anno_acquisto},{self.valore}"

class Prestito: #creo la classe prestito per la quinta funzione
    def __init__(self,id_prestito,data,id_strumento,cognome_allievo):
        self.id_prestito=id_prestito
        self.data=data
        self.id_strumento=id_strumento
        self.cognome_allievo=cognome_allievo

    def __str__(self):
        return f"{self.id_prestito}, {self.data}, {self.id_strumento}, {self.cognome_allievo}"



class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome=nome
        self._responsabile=responsabile
        self.strumenti=[] #creo una collezione di oggetti all'interno di una classe
        self.prestiti=[] #creo lista per iterare sui prestiti

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        if nuovo_responsabile.strip()=="": #mi assicuro che il nome del nuovo responsabile sia corretto
            raise ValueError("Responsabile incorretto")
        self._responsabile=nuovo_responsabile


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
        id_prestito="P"+str(len(self.prestiti)+1) #numero i prestiti
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
