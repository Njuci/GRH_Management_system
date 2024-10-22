
from tkinter.messagebox import showerror,showinfo

class Agent:
    def __init__(self,nom_agent,sexe,date_naiss,lieu_naiss,etat_civil,adresse,nombre_enfant ):
        self.nom_dom = nom_agent
        self.sexe=sexe
        self.date_naiss=date_naiss
        self.lieu_naiss=lieu_naiss
        self.etat_civil=etat_civil
        self.adresse=adresse
        self.nombre_enfant=nombre_enfant
    def get_all(self,curseur):
        try:
            curseur.execute("select * from agent order by(-id_agent)")
            return curseur.fetchall()
        except Exception as e:
            showerror("Erreur",str(e))
            return False
        
    def save(self, curseur):
        try:
            # Requête d'insertion
            query = """
            INSERT INTO Agent (nom, sexe, date_naissance, lieu_naissance, etat_civil, adresse, nombre_enfant)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            # Exécution de la requête
            curseur.execute(query, (self.nom_dom, self.sexe, self.date_naiss, self.lieu_naiss, self.etat_civil, self.adresse, self.nombre_enfant))
            return True
        except Exception as e:
            # Affichage de l'erreur et des données refusées
            print("Erreur:", str(e))
            print("Données refusées:", self.nom_dom, self.sexe, self.date_naiss, self.lieu_naiss, self.etat_civil, self.adresse, self.nombre_enfant)
            showerror("Erreur", str(e))
            return False 
"""    def update(self,curseur,id):
        try:
            curseur.execute("update domaine_cours set nom_dom=%s where id_dom=%s",(self.nom_dom,id))
            return True
        except Exception as e:
            showerror("Erreur",str(e))
            return False
    def delete(self,curseur,id):
        try:
            curseur.execute("delete from domaine_cours where id_dom=%s",(id,))
            return True
        except Exception as e:
            showerror("Erreur",str(e))
            return False
   """
