import mysql.connector 
from tkinter.messagebox import showerror,showinfo

class Connexion:
    def __init__(self):
        #completer les parametres de connexion avexc le fichier parametre.cnf
        #les parametres sont host,user,password,database
       
        try:
            self.db = mysql.connector.connect(
            host = 'localhost',
            user = 'njuci',
            password = '3670njci',
            database = 'Gestion_Ressources_Humaines',
            autocommit=True
        )
            self.curseur=self.db.cursor()
        except Exception as e:
            showerror("Erreur",'Erreur de connexion à la base de données')
            #faire la configuration
            self.db=None
            
    def login(self):
        try:
            if self.db.is_connected():
                 return True
        except Exception as e:
            showerror("Erreur",str(e)) 
            return False     

    def get_curseur(self):
        return self.curseur                 
    def get_connexion(self):
        return self.curseur
    def get_parametres_connexion(self):
        return self.db
    def close(self):
        self.db.close()
        self.curseur.close()