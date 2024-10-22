from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from backend.barene_backend import BaremeSalariale
from backend.fonction_backend import Fonction

class BaremeSalarialeGestFrontend:
    def __init__(self, parent_frame, curseur):
        self.parent_frame = parent_frame
        self.baremes = []  # Liste pour stocker les barèmes localement
        self.fonctions = []  # Liste pour stocker les fonctions localement
        self.bg = '#FFFFFF'
        self.curseur = curseur
        self.succes_colors = '#27B795'
        self.bleck_color = '#000000'
        
        # Section des barèmes salariaux
        self.BaremeSection = tk.Frame(self.parent_frame, height=700, bg=self.bg, width=760, relief="groove")
        self.BaremeSection.place(x=10, y=20)
       
        # Formulaire de gestion des barèmes salariaux
        self.form = tk.Frame(self.BaremeSection, height=200, width=750, relief="groove", bg=self.bg)
        self.form.place(x=5, y=20)

        self.TitleForm = tk.Label(self.form, text='GESTION DES BAREMES SALARIAUX', bg=self.bg, font='Arial 14', fg=self.bleck_color)
        self.TitleForm.place(x=200, y=20, height=30)

        # Champs du formulaire
        self.SalaireLab = tk.Label(self.form, text='Salaire Horaire', bg='white', font='12')
        self.SalaireLab.place(x=60, y=70, height=30)
        self.SalaireEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.SalaireEnt.place(x=220, y=70, width=200, height=30)

        self.FonctionLab = tk.Label(self.form, text='Fonction', bg='white', font='12')
        self.FonctionLab.place(x=60, y=110, height=30)
        self.FonctionCombo = ttk.Combobox(self.form, values=self.get_fonctions())
        self.FonctionCombo.place(x=220, y=110, width=200, height=30)

        # Boutons
        self.Ajouter_btn = tk.Button(self.BaremeSection, bg=self.succes_colors, text='AJOUTER', fg='white', relief="flat", font="Arial 9", command=self.ajouter_bareme)
        self.Ajouter_btn.place(x=200, y=180, width=100, height=30)

        self.Supprimer_btn = tk.Button(self.BaremeSection, bg='red', text='SUPPRIMER', fg='white', relief="flat", font="Arial 9", command=self.supprimer_bareme)
        self.Supprimer_btn.place(x=310, y=180, width=100, height=30)

        self.Modifier_btn = tk.Button(self.BaremeSection, bg='#4CAF50', text='MODIFIER', fg='white', relief="flat", font="Arial 9", command=self.modifier_bareme)
        self.Modifier_btn.place(x=420, y=180, width=100, height=30)

        self.Imprimer_btn = tk.Button(self.BaremeSection, bg='orange', text='IMPRIMER', fg='white', relief="flat", font="Arial 9", command=self.imprimer_bareme)
        self.Imprimer_btn.place(x=530, y=180, width=100, height=30)

        # Section du tableau
        self.TabSection = tk.Frame(self.BaremeSection, height=350, width=740, relief="groove")
        self.TabSection.place(x=0, y=230)

        # Ajout des barres de défilement
        self.scroll_x = ttk.Scrollbar(self.TabSection, orient=tk.HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.TabSection, orient=tk.VERTICAL)

        # Tableau avec colonnes
        self.tableau = ttk.Treeview(self.TabSection, columns=('N°', 'ID', 'Salaire Horaire', 'Date Fixation', 'Fonction'), 
                                    show='headings', xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Configuration des colonnes du tableau
        self.tableau.heading('N°', text='N°')
        self.tableau.heading('ID', text='ID')
        self.tableau.heading('Salaire Horaire', text='Salaire Horaire')
        self.tableau.heading('Date Fixation', text='Date Fixation')
        self.tableau.heading('Fonction', text='Fonction')

        self.tableau.column('N°', width=40, anchor='center')
        self.tableau.column('ID', width=100, anchor='center')
        self.tableau.column('Salaire Horaire', width=100, anchor='center')
        self.tableau.column('Date Fixation', width=100, anchor='center')
        self.tableau.column('Fonction', width=200, anchor='center')

        # Placement du tableau et des barres de défilement
        self.tableau.place(x=0, y=0, width=720, height=320)
        self.scroll_x.place(x=0, y=320, width=720)
        self.scroll_y.place(x=720, y=0, height=320)

        self.scroll_x.config(command=self.tableau.xview)
        self.scroll_y.config(command=self.tableau.yview)
        self.afficher()

    def get_fonctions(self):
        fonction = Fonction("", "")
        data = fonction.get_all(self.curseur)
        self.fonctions = {row[1]+'|'+row[2] : row[0] for row in data}  # Dictionnaire {nom: id}
        return list(self.fonctions.keys())

    def ajouter_bareme(self):
        # Récupérer les informations des champs
        salaire_horaire = self.SalaireEnt.get()
        nom_fonction = self.FonctionCombo.get()
        id_fonction = self.fonctions.get(nom_fonction)

        # Validation simple
        if not (salaire_horaire and id_fonction):
            showinfo('Erreur', 'Veuillez remplir tous les champs')
            return

        bareme = BaremeSalariale(salaire_horaire, id_fonction)
        if bareme.save(self.curseur):
            showinfo('Succès', 'Barème ajouté avec succès')
            self.afficher()
            self.clean()

    def clean(self):
        # Réinitialiser les champs
        self.SalaireEnt.delete(0, tk.END)
        self.FonctionCombo.set('')
        
    def afficher(self):
        bareme = BaremeSalariale("", "")
        data = bareme.get_all(self.curseur)
        
        self.tableau.delete(*self.tableau.get_children())
        cpt = 0

        for row in data:
            cpt += 1
            self.tableau.insert('', 'end', values=(cpt, row[0], row[1], row[2], row[3]))
        
        # Bind double click to get selected row data
        self.tableau.bind('<Double-Button-1>', self.get_selection)

    def get_selection(self, event):
        selected_item = self.tableau.selection()[0]
        values = self.tableau.item(selected_item, 'values')

        # Populate the form fields with the selected row's data
        self.SalaireEnt.delete(0, tk.END)
        self.SalaireEnt.insert(0, values[2])
        self.FonctionCombo.set(values[4])
   
    # Méthode pour avoir les informations des entry et returner les valeurs sous forme de liste
    def get_values(self):
        salaire_horaire = self.SalaireEnt.get()
        nom_fonction = self.FonctionCombo.get()
        id_fonction = self.fonctions.get(nom_fonction)
        return [salaire_horaire, id_fonction]
   
    # Méthode pour modifier un barème
    def modifier_bareme(self):
        # Récupérer les informations des champs
        salaire_horaire, id_fonction = self.get_values()

        # Validation simple
        if not (salaire_horaire and id_fonction):
            showinfo('Erreur', 'Veuillez remplir tous les champs')
            return

        id = self.get_selected_bareme_id()
        if id is not None:
            bareme = BaremeSalariale(salaire_horaire, id_fonction)
            if bareme.update(self.curseur, id):
                showinfo('Succès', 'Barème modifié avec succès')

        # Afficher les barèmes
        self.afficher()
        self.clean()

    def get_selected_bareme_id(self):
        try:
            # Vérifie s'il y a une sélection
            selected_item = self.tableau.selection()
            
            if not selected_item:
                showinfo("Aucune sélection", "Veuillez sélectionner une ligne.")
                return None

            # Si une ligne est sélectionnée, récupérer l'ID du barème
            selected_item = selected_item[0]  # Prendre le premier élément sélectionné
            bareme_id = self.tableau.item(selected_item, 'values')[1]
            return bareme_id

        except IndexError:
            showinfo("Erreur", "La sélection est invalide.")
            return None

    def supprimer_bareme(self):
        id = self.get_selected_bareme_id()
        if id is not None:
            bareme = BaremeSalariale("", "")
            if bareme.delete(self.curseur, id):
                showinfo('Succès', 'Barème supprimé avec succès')
                self.afficher()
                self.clean()

    # Méthode pour imprimer tous les barèmes
    def imprimer_bareme(self):
        pass

# Exemple d'util