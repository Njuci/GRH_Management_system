from tkinter.messagebox import showerror


class Departement:
    def __init__(self, nom_depart):
        self.nom_depart = nom_depart

    def save(self, curseur):
        try:
            curseur.execute("INSERT INTO Departement (nom_depart) VALUES (%s)", (self.nom_depart,))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def update(self, curseur, id):
        try:
            curseur.execute("UPDATE Departement SET nom_depart=%s WHERE id_departement=%s", (self.nom_depart, id))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def delete(self, curseur, id):
        try:
            curseur.execute("DELETE FROM Departement WHERE id_departement=%s", (id,))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def get_all(self, curseur):
        try:
            curseur.execute("SELECT * FROM Departement")
            return curseur.fetchall()
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return []