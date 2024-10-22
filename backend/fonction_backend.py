from tkinter.messagebox import showerror

class Fonction:
    def __init__(self, nom_fonction, id_departement):
        self.nom_fonction = nom_fonction
        self.id_departement = id_departement

    def save(self, curseur):
        try:
            curseur.execute("INSERT INTO Fonction (nom_fonction, id_departement) VALUES (%s, %s)", (self.nom_fonction, self.id_departement))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def update(self, curseur, id):
        try:
            curseur.execute("UPDATE Fonction SET nom_fonction=%s, id_departement=%s WHERE id_fonction=%s", (self.nom_fonction, self.id_departement, id))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def delete(self, curseur, id):
        try:
            curseur.execute("DELETE FROM Fonction WHERE id_fonction=%s", (id,))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def get_all(self, curseur):
        try:
            curseur.execute("""
                SELECT f.id_fonction, f.nom_fonction, d.nom_depart
                FROM Fonction f
                LEFT JOIN Departement d ON f.id_departement = d.id_departement
            """)
            return curseur.fetchall()
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return []