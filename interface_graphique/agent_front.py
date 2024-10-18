import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from datetime import datetime
from backend.agent_backend import Agent

class AgentGestFrontend:
    def __init__(self, parent_frame, curseur):
        self.parent_frame = parent_frame
        self.agents = []  # Liste pour stocker les agents localement
        self.bg = '#FFFFFF'
        self.curseur = curseur
        self.succes_colors = '#27B795'
        self.bleck_color = '#000000'
        
        # Section des agents
        self.AgentSection = tk.Frame(self.parent_frame, height=700, bg=self.bg, width=760, relief="groove")
        self.AgentSection.place(x=10, y=20)
       
        # Formulaire de gestion des agents
        self.form = tk.Frame(self.AgentSection, height=400, width=750, relief="groove", bg=self.bg)
        self.form.place(x=5, y=20)

        self.TitleForm = tk.Label(self.form, text='GESTION DES AGENTS', bg=self.bg, font='Arial 14', fg=self.bleck_color)
        self.TitleForm.place(x=280, y=20, height=30)

        # Champs du formulaire
        self.NomLab = tk.Label(self.form, text='Nom', bg='white', font='12')
        self.NomLab.place(x=60, y=70, height=30)
        self.NomEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.NomEnt.place(x=180, y=70, width=200, height=30)

        self.SexeLab = tk.Label(self.form, text='Sexe', bg='white', font='12')
        self.SexeLab.place(x=400, y=70, height=30)
        self.SexeCombo = ttk.Combobox(self.form, values=['Homme', 'Femme'])
        self.SexeCombo.place(x=500, y=70, width=200, height=30)

        self.DateNaissLab = tk.Label(self.form, text='Date Naissance', bg='white', font='12')
        self.DateNaissLab.place(x=60, y=110, height=30)
        self.DateNaissEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.DateNaissEnt.place(x=180, y=110, width=200, height=30)

        self.LieuNaissLab = tk.Label(self.form, text='Lieu Naissance', bg='white', font='12')
        self.LieuNaissLab.place(x=400, y=110, height=30)
        self.LieuNaissEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.LieuNaissEnt.place(x=520, y=110, width=180, height=30)

        self.EtatCivilLab = tk.Label(self.form, text='Etat Civil', bg='white', font='12')
        self.EtatCivilLab.place(x=60, y=150, height=30)
        self.EtatCivilCombo = ttk.Combobox(self.form, values=['Célibataire', 'Marié(e)', 'Divorcé(e)', 'Veuf/Veuve'])
        self.EtatCivilCombo.place(x=180, y=150, width=200, height=30)

        self.AdresseLab = tk.Label(self.form, text='Adresse', bg='white', font='12')
        self.AdresseLab.place(x=400, y=150, height=30)
        self.AdresseEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.AdresseEnt.place(x=500, y=150, width=200, height=30)

        self.EnfantsLab = tk.Label(self.form, text="Nombre d'enfants", bg='white', font='12')
        self.EnfantsLab.place(x=60, y=190, height=30)
        self.EnfantsEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.EnfantsEnt.place(x=200, y=190, width=180, height=30)

        # Boutons
        self.Ajouter_btn = tk.Button(self.AgentSection, bg=self.succes_colors, text='AJOUTER', fg='white', relief="flat", font="Arial 9", command=self.ajouter_agent)
        self.Ajouter_btn.place(x=400, y=270, width=100, height=30)

        self.Supprimer_btn = tk.Button(self.AgentSection, bg='red', text='SUPPRIMER', fg='white', relief="flat", font="Arial 9")
        self.Supprimer_btn.place(x=510, y=270, width=100, height=30)

        # Section du tableau
        self.TabSection = tk.Frame(self.AgentSection, height=250, width=740, relief="groove")
        self.TabSection.place(x=0, y=310)

        # Ajout des barres de défilement
        self.scroll_x = ttk.Scrollbar(self.TabSection, orient=tk.HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.TabSection, orient=tk.VERTICAL)

        # Tableau avec colonnes
        self.tableau = ttk.Treeview(self.TabSection, columns=('N°','ID','Nom', 'Sexe', 'Date Naissance', 'Lieu Naissance', 'Etat Civil', 'Adresse', 'Enfants'), 
                                    show='headings', xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Configuration des colonnes du tableau
        self.tableau.heading('N°', text='N°')
        self.tableau.heading('ID', text='ID')
        self.tableau.heading('Nom', text='Nom')
        self.tableau.heading('Sexe', text='Sexe')
        self.tableau.heading('Date Naissance', text='Date Naissance')
        self.tableau.heading('Lieu Naissance', text='Lieu Naissance')
        self.tableau.heading('Etat Civil', text='Etat Civil')
        self.tableau.heading('Adresse', text='Adresse')
        self.tableau.heading('Enfants', text='Enfants')

        self.tableau.column('N°', width=40, anchor='center')
        self.tableau.column('ID', width=100, anchor='center')
        self.tableau.column('Nom', width=100, anchor='center')
        self.tableau.column('Sexe', width=100, anchor='center')
        self.tableau.column('Date Naissance', width=120, anchor='center')
        self.tableau.column('Lieu Naissance', width=120, anchor='center')
        self.tableau.column('Etat Civil', width=100, anchor='center')
        self.tableau.column('Adresse', width=150, anchor='center')
        self.tableau.column('Enfants', width=80, anchor='center')

        # Placement du tableau et des barres de défilement
        self.tableau.place(x=0, y=0, width=720, height=530)
        self.scroll_x.place(x=0, y=530, width=720)
        self.scroll_y.place(x=400, y=0, height=530)

        self.scroll_x.config(command=self.tableau.xview)
        self.scroll_y.config(command=self.tableau.yview)

    def ajouter_agent(self):
        # Récupérer les informations des champs
        nom = self.NomEnt.get()
        sexe = self.SexeCombo.get()
        date_naissance = self.DateNaissEnt.get()
        lieu_naissance = self.LieuNaissEnt.get()
        etat_civil = self.EtatCivilCombo.get()
        adresse = self.AdresseEnt.get()
        enfants = self.EnfantsEnt.get()

        # Validation simple
        if not (nom and sexe and date_naissance and lieu_naissance and etat_civil and adresse and enfants):
            showinfo('Erreur', 'Veuillez remplir tous les champs')
            return

        try:
            # Vérifier la date
            datetime.strptime(date_naissance, '%Y-%m-%d')
        except ValueError:
            showinfo('Erreur', 'Format de date incorrect (attendu : YYYY-MM-DD)')
            return

    def cleam(self):
        # Réinitialiser les champs
        self.NomEnt.delete(0, tk.END)
        self.SexeCombo.set('')
        self.DateNaissEnt.delete(0, tk.END)
        self.LieuNaissEnt.delete(0, tk.END)
        self.EtatCivilCombo.set('')
        self.AdresseEnt.delete(0, tk.END)
        self.EnfantsEnt.delete(0, tk.END)
        
    def afficher(self):
        assign = Agent("", "", "", "", "", "", "")
        data = assign.get_all(self.curseur)
        
        self.tableau.delete(*self.tableau.get_children())
        cpt = 0

        for row in data:
            cpt += 1
            self.tableau.insert('', 'end', values=(cpt, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        self.tableau.bind('<Double-Button-1>', self.get_selection)