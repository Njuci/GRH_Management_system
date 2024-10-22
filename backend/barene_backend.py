from tkinter.messagebox import showerror
class BaremeSalariale:
    def __init__(self, salaire_horaire, id_fonction):
        self.salaire_horaire = salaire_horaire
        self.id_fonction = id_fonction

    def save(self, curseur):
        try:
            curseur.execute("INSERT INTO Bareme_salariale (salaire_horaire, id_fonction) VALUES (%s, %s)", (self.salaire_horaire, self.id_fonction))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def update(self, curseur, id):
        try:
            curseur.execute("UPDATE Bareme_salariale SET salaire_horaire=%s, id_fonction=%s WHERE id_bareme=%s", (self.salaire_horaire, self.id_fonction, id))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def delete(self, curseur, id):
        try:
            curseur.execute("DELETE FROM Bareme_salariale WHERE id_bareme=%s", (id,))
            return True
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return False

    def get_all(self, curseur):
        try:
            curseur.execute("""
                SELECT b.id_bareme, b.salaire_horaire, b.date_fixation, f.nom_fonction
                FROM Bareme_salariale b
                LEFT JOIN Fonction f ON b.id_fonction = f.id_fonction
            """)
            return curseur.fetchall()
        except Exception as e:
            print(str(e))
            showerror("Erreur", str(e))
            return []