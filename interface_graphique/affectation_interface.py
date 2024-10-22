from datetime import datetime,date
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from backend.affectation_backend import Affectation
from backend.agent_backend import Agent
from backend.fonction_backend import Fonction

class AffectationGestFrontend:
    def __init__(self, parent_frame, curseur):
        self.parent_frame = parent_frame
        self.affectations = []  # Liste pour stocker les affectations localement
        self.agents = []  # Liste pour stocker les agents localement
        self.fonctions = []  # Liste pour stocker les fonctions localement
        self.bg = '#FFFFFF'
        self.curseur = curseur
        self.succes_colors = '#27B795'
        self.bleck_color = '#000000'
        
        # Section des affectations
        self.AffectationSection = tk.Frame(self.parent_frame, height=700, bg=self.bg, width=760, relief="groove")
        self.AffectationSection.place(x=10, y=20)
       
        # Formulaire de gestion des affectations
        self.form = tk.Frame(self.AffectationSection, height=200, width=750, relief="groove", bg=self.bg)
        self.form.place(x=5, y=20)

        self.TitleForm = tk.Label(self.form, text='GESTION DES AFFECTATIONS', bg=self.bg, font='Arial 14', fg=self.bleck_color)
        self.TitleForm.place(x=200, y=20, height=30)

        # Champs du formulaire
        self.AgentLab = tk.Label(self.form, text='Agent', bg='white', font='12')
        self.AgentLab.place(x=10, y=70, height=30)
        self.AgentCombo = ttk.Combobox(self.form, values=self.get_agents())
        self.AgentCombo.place(x=170, y=70, width=150, height=30)

        self.FonctionLab = tk.Label(self.form, text='Fonction', bg='white', font='12')
        self.FonctionLab.place(x=10, y=110, height=30)
        self.FonctionCombo = ttk.Combobox(self.form, values=self.get_fonctions())
        self.FonctionCombo.place(x=170, y=110, width=200, height=30)

        self.DateDebutLab = tk.Label(self.form, text='Date Début', bg='white', font='12')
        self.DateDebutLab.place(x=10, y=150, height=30)
        self.DateDebutEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.DateDebutEnt.insert(0, 'YYYY-MM-DD')  # Placeholder pour le format de la date
        self.DateDebutEnt.place(x=170, y=150, width=200, height=30)

        self.DateFinLab = tk.Label(self.form, text='Date Fin', bg='white', font='12')
        self.DateFinLab.place(x=350, y=70, height=30)
        self.DateFinEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.DateFinEnt.insert(0, 'YYYY-MM-DD')  # Placeholder pour le format de la date
        self.DateFinEnt.place(x=430, y=70, width=200, height=30)

        # Boutons
        self.Ajouter_btn = tk.Button(self.AffectationSection, bg=self.succes_colors, text='AJOUTER', fg='white', relief="flat", font="Arial 9", command=self.ajouter_affectation)
        self.Ajouter_btn.place(x=200, y=250, width=100, height=30)

        self.Supprimer_btn = tk.Button(self.AffectationSection, bg='red', text='SUPPRIMER', fg='white', relief="flat", font="Arial 9", command=self.supprimer_affectation)
        self.Supprimer_btn.place(x=310, y=250, width=100, height=30)

        self.Modifier_btn = tk.Button(self.AffectationSection, bg='#4CAF50', text='MODIFIER', fg='white', relief="flat", font="Arial 9", command=self.modifier_affectation)
        self.Modifier_btn.place(x=420, y=250, width=100, height=30)

        self.Imprimer_btn = tk.Button(self.AffectationSection, bg='orange', text='IMPRIMER', fg='white', relief="flat", font="Arial 9", command=self.imprimer_affectation)
        self.Imprimer_btn.place(x=530, y=250, width=100, height=30)

        # Section du tableau
        self.TabSection = tk.Frame(self.AffectationSection, height=300, width=740, relief="groove")
        self.TabSection.place(x=0, y=300)

        # Ajout des barres de défilement
        self.scroll_x = ttk.Scrollbar(self.TabSection, orient=tk.HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.TabSection, orient=tk.VERTICAL)

        # Tableau avec colonnes
        self.tableau = ttk.Treeview(self.TabSection, columns=('N°', 'ID', 'Agent', 'Fonction', 'Date Début', 'Date Fin'), 
                                    show='headings', xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Configuration des colonnes du tableau
        self.tableau.heading('N°', text='N°')
        self.tableau.heading('ID', text='ID')
        self.tableau.heading('Agent', text='Agent')
        self.tableau.heading('Fonction', text='Fonction')
        self.tableau.heading('Date Début', text='Date Début')
        self.tableau.heading('Date Fin', text='Date Fin')

        self.tableau.column('N°', width=40, anchor='center')
        self.tableau.column('ID', width=100, anchor='center')
        self.tableau.column('Agent', width=100, anchor='center')
        self.tableau.column('Fonction', width=150, anchor='center')
        self.tableau.column('Date Début', width=100, anchor='center')
        self.tableau.column('Date Fin', width=100, anchor='center')

        # Placement du tableau et des barres de défilement
        self.tableau.place(x=0, y=0, width=720, height=280)
        self.scroll_x.place(x=0, y=280, width=720)
        self.scroll_y.place(x=720, y=0, height=280)

        self.scroll_x.config(command=self.tableau.xview)
        self.scroll_y.config(command=self.tableau.yview)
        self.afficher()

    def get_agents(self):
        agent = Agent("", "",  "", "", "", "", 0)
        data = agent.get_all(self.curseur)
        self.agents = {row[1]: row[0] for row in data}  # Dictionnaire {nom: id}
        return list(self.agents.keys())

    def get_fonctions(self):
        fonction = Fonction("", "")
        data = fonction.get_all(self.curseur)
        self.fonctions = {row[1]+'|'+row[2] : row[0] for row in data}  # Dictionnaire {nom: id}
        return list(self.fonctions.keys())

    def ajouter_affectation(self):
        # Récupérer les informations des champs
        nom_agent = self.AgentCombo.get()
        id_agent = self.agents.get(nom_agent)
        nom_fonction = self.FonctionCombo.get()
        id_fonction = self.fonctions.get(nom_fonction)
        date_debut = self.DateDebutEnt.get()
        date_fin = self.DateFinEnt.get()

        # Validation simple
        if not (id_agent and id_fonction and date_debut):
            showinfo('Erreur', 'Veuillez remplir tous les champs obligatoires')
            return

        try:
            # Vérifier les dates
            datetime.strptime(date_debut, '%Y-%m-%d')
            if date_fin:
                datetime.strptime(date_fin, '%Y-%m-%d')
        except ValueError:
            showinfo('Erreur', 'Format de date incorrect (attendu : YYYY-MM-DD)')
            return

        # Vérifier les conflits d'affectation
        if self.verifier_conflit_affectation(id_agent, date_debut, date_fin):
            showinfo('Erreur', 'L\'agent a déjà une affectation en cours pendant cette période')
            return

        affectation = Affectation(id_agent, id_fonction, date_debut, date_fin)
        if affectation.save(self.curseur):
            showinfo('Succès', 'Affectation ajoutée avec succès')
            self.afficher()
            self.clean()
    def verifier_conflit_affectation(self, id_agent, date_debut, date_fin):
        affectation = Affectation("", "", "", "")
        data = affectation.get_affectations_by_agent(self.curseur, id_agent)
       
        
        # Convertir les dates de début et de fin en objets datetime.date
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date() if date_fin else None
        
        for row in data:
            # Vérifier si row[2] et row[3] sont déjà des objets datetime.date
            row_date_debut = row[1] if isinstance(row[1], date) else datetime.strptime(row[1], '%Y-%m-%d').date()
            row_date_fin = row[2] if isinstance(row[2], date) else datetime.strptime(row[2], '%Y-%m-%d').date() if row[2] else None
            
            if (date_fin and row_date_debut <= date_fin and row_date_fin >= date_debut) or (not date_fin and row_date_fin >= date_debut):
                return True
        return False
    def clean(self):
        # Réinitialiser les champs
        self.AgentCombo.set('')
        self.FonctionCombo.set('')
        self.DateDebutEnt.delete(0, tk.END)
        self.DateDebutEnt.insert(0, 'YYYY-MM-DD')  # Placeholder pour le format de la date
        self.DateFinEnt.delete(0, tk.END)
        self.DateFinEnt.insert(0, 'YYYY-MM-DD')  # Placeholder pour le format de la date
        
    def afficher(self):
        affectation = Affectation("", "", "", "")
        data = affectation.get_all(self.curseur)
        
        self.tableau.delete(*self.tableau.get_children())
        cpt = 0

        for row in data:
            cpt += 1
            self.tableau.insert('', 'end', values=(cpt, row[0], row[1], row[2]+'|'+row[5] , row[3], row[4]))
        
        # Bind double click to get selected row data
        self.tableau.bind('<Double-Button-1>', self.get_selection)

    def get_selection(self, event):
        selected_item = self.tableau.selection()[0]
        values = self.tableau.item(selected_item, 'values')

        # Populate the form fields with the selected row's data
        self.AgentCombo.set(values[2])
        self.FonctionCombo.set(values[3])
        self.DateDebutEnt.delete(0, tk.END)
        self.DateDebutEnt.insert(0, values[4])
        self.DateFinEnt.delete(0, tk.END)
        if values[5] != 'None':
            self.DateFinEnt.insert(0, values[5])
   
    # Méthode pour avoir les informations des entry et returner les valeurs sous forme de liste
    def get_values(self):
        nom_agent = self.AgentCombo.get()
        id_agent = self.agents.get(nom_agent)
        nom_fonction = self.FonctionCombo.get()
        id_fonction = self.fonctions.get(nom_fonction)
        date_debut = self.DateDebutEnt.get()
        date_fin = self.DateFinEnt.get()
        return [id_agent, id_fonction, date_debut, date_fin]
   
    # Méthode pour modifier une affectation
    def modifier_affectation(self):
        # Récupérer les informations des champs
        id_agent, id_fonction, date_debut, date_fin = self.get_values()

        # Validation simple
        if not (id_agent and id_fonction and date_debut):
            showinfo('Erreur', 'Veuillez remplir tous les champs obligatoires')
            return

        try:
            # Vérifier les dates
            datetime.strptime(date_debut, '%Y-%m-%d')
            if date_fin:
                datetime.strptime(date_fin, '%Y-%m-%d')
        except ValueError:
            showinfo('Erreur', 'Format de date incorrect (attendu : YYYY-MM-DD)')
            return

        id = self.get_selected_affectation_id()
        if id is not None:
            affectation = Affectation(id_agent, id_fonction, date_debut, date_fin)
            if affectation.update(self.curseur, id):
                showinfo('Succès', 'Affectation modifiée avec succès')

        # Afficher les affectations
        self.afficher()
        self.clean()

    def get_selected_affectation_id(self):
        try:
            # Vérifie s'il y a une sélection
            selected_item = self.tableau.selection()
            
            if not selected_item:
                showinfo("Aucune sélection", "Veuillez sélectionner une ligne.")
                return None

            # Si une ligne est sélectionnée, récupérer l'ID de l'affectation
            selected_item = selected_item[0]  # Prendre le premier élément sélectionné
            affectation_id = self.tableau.item(selected_item, 'values')[1]
            return affectation_id

        except IndexError:
            showinfo("Erreur", "La sélection est invalide.")
            return None

    def supprimer_affectation(self):
        id = self.get_selected_affectation_id()
        if id is not None:
            affectation = Affectation("", "", "", "")
            if affectation.delete(self.curseur, id):
                showinfo('Succès', 'Affectation supprimée avec succès')
                self.afficher()
                self.clean()

    # Méthode pour imprimer toutes les affectations
    def imprimer_affectation(self):
        pass
