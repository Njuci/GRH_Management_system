from tkinter.messagebox import showerror
class Affectation:
    def __init__(self, id_agent, id_fonction, date_debut, date_fin):
        self.id_agent = id_agent
        self.id_fonction = id_fonction
        self.date_debut = date_debut
        self.date_fin = date_fin

    def save(self, curseur):
        try:
            curseur.execute("INSERT INTO Affecter (id_agent, id_fonction, date_debut, date_fin) VALUES (%s, %s, %s, %s)", 
                            (self.id_agent, self.id_fonction, self.date_debut, self.date_fin))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def update(self, curseur, id):
        try:
            curseur.execute("UPDATE Affecter SET id_agent=%s, id_fonction=%s, date_debut=%s, date_fin=%s WHERE id_affectation=%s", 
                            (self.id_agent, self.id_fonction, self.date_debut, self.date_fin, id))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def delete(self, curseur, id):
        try:
            curseur.execute("DELETE FROM Affecter WHERE id_affectation=%s", (id,))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def get_all(self, curseur):
        try:
            curseur.execute("""
                SELECT a.id_affectation, ag.nom, f.nom_fonction, a.date_debut, a.date_fin, d.nom_depart
                FROM Affecter a
                LEFT JOIN Agent ag ON a.id_agent = ag.id_agent
                LEFT JOIN Fonction f ON a.id_fonction = f.id_fonction
                LEFT JOIN Departement d ON f.id_departement = d.id_departement
            """)
            return curseur.fetchall()
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return []

    def get_affectations_by_agent(self, curseur, id_agent):
        try:
            curseur.execute("SELECT * FROM Affecter WHERE id_agent=%s", (id_agent,))
            return curseur.fetchall()
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return []