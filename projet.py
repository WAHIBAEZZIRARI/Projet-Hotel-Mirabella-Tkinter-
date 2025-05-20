import tkinter as tk
from tkinter import messagebox, Listbox
import csv

#  Fenêtre principale 
root = tk.Tk()
root.title("HOTEL MIRABELLA")
root.geometry("500x600")
root.configure(bg="#0c1b33")

#  Zone d'en-tête 
tk.Label(root, text="HOTEL\nMIRABELLA", font=("Georgia", 22, "bold"), bg="#0c1b33", fg="gold").pack()

titre_label = tk.Label(root, text="", font=("Arial", 18, "bold"), bg="#0c1b33", fg="white")
titre_label.pack(pady=(30, 10))

frame = tk.Frame(root, bg="#0c1b33")
frame.pack()

# Variables globales
nom_entry = None
type_chambre = None
num_chambre = None
jours_entry = None
listbox = None

def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

#  Page de connexion 
def afficher_connexion():
    clear_frame()
    titre_label.config(text="Connexion")

    tk.Label(frame, text="Email", bg="#0c1b33", fg="white", anchor='w').pack(padx=40, anchor='w')
    email_entry = tk.Entry(frame, width=30)
    email_entry.pack(padx=40, pady=5)

    tk.Label(frame, text="Mot de passe", bg="#0c1b33", fg="white", anchor='w').pack(padx=40, anchor='w')
    motdepasse_entry = tk.Entry(frame, width=30, show="*")
    motdepasse_entry.pack(padx=40, pady=5)

    def se_connecter():
        if email_entry.get() == "admin@mirabella.com" and motdepasse_entry.get() == "1234":
            messagebox.showinfo("Bienvenue", "Connexion réussie !")
            afficher_reservation()
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")

    tk.Button(frame, text="Se connecter", bg="#d4a857", fg="black", font=("Arial", 12, "bold"), command=se_connecter).pack(pady=20)

#  Page de réservation 
def afficher_reservation():
    global nom_entry, type_chambre, num_chambre, jours_entry, listbox

    clear_frame()
    titre_label.config(text="Réserver une chambre")

    # Nom
    tk.Label(frame, text="Nom complet", bg="#0c1b33", fg="white").pack(padx=40, anchor='w')
    nom_entry = tk.Entry(frame, width=30)
    nom_entry.pack(padx=40, pady=5)

    # Type de chambre
    tk.Label(frame, text="Type de chambre", bg="#0c1b33", fg="white").pack(padx=40, anchor='w')
    type_chambre = tk.StringVar(value="Simple")

    radio_frame = tk.Frame(frame, bg="#0c1b33")
    radio_frame.pack(padx=40, pady=5, anchor='w')

    tk.Radiobutton(radio_frame, text="Simple", variable=type_chambre, value="Simple",
                   bg="#0c1b33", fg="white", selectcolor="#d4a857").pack(side="left", padx=5)
    tk.Radiobutton(radio_frame, text="Double", variable=type_chambre, value="Double",
                   bg="#0c1b33", fg="white", selectcolor="#d4a857").pack(side="left", padx=5)
    tk.Radiobutton(radio_frame, text="Suite", variable=type_chambre, value="Suite",
                   bg="#0c1b33", fg="white", selectcolor="#d4a857").pack(side="left", padx=5)

    # Numéro chambre
    tk.Label(frame, text="Numéro de chambre", bg="#0c1b33", fg="white").pack(padx=40, anchor='w')
    num_chambre = tk.Entry(frame, width=30)
    num_chambre.pack(padx=40, pady=5)

    # Nombre de jours
    tk.Label(frame, text="Nombre de jours", bg="#0c1b33", fg="white").pack(padx=40, anchor='w')
    jours_entry = tk.Entry(frame, width=30)
    jours_entry.pack(padx=40, pady=5)

    # Liste
    listbox = Listbox(frame, width=60)
    listbox.pack(pady=10)

    # Fonctions
    def reserver():
        nom = nom_entry.get()
        chambre = type_chambre.get()
        num = num_chambre.get()
        jours = jours_entry.get()

        if not (nom and chambre and num and jours):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            with open("fichier.csv", "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([nom, chambre, num, jours])
            messagebox.showinfo("Succès", "Réservation confirmée")
            afficher()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def afficher():
        listbox.delete(0, tk.END)
        try:
            with open("fichier.csv", "r", newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=";")
                for ligne in reader:
                    listbox.insert(tk.END, " | ".join(ligne))
        except FileNotFoundError:
            messagebox.showwarning("Fichier manquant", "Aucune réservation enregistrée.")

    def supprimer():
        nom = nom_entry.get()
        if not nom:
            messagebox.showerror("Erreur", "Entrez le nom pour supprimer la réservation.")
            return

        nouvelle_liste = []
        supprime = False
        try:
            with open("fichier.csv", "r", newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=";")
                for ligne in reader:
                    if ligne and nom.lower() not in ligne[0].lower():
                        nouvelle_liste.append(ligne)
                    else:
                        supprime = True

            if supprime:
                with open("fichier.csv", "w", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerows(nouvelle_liste)
                messagebox.showinfo("Succès", "Réservation(s) supprimée(s).")
                afficher()
            else:
                messagebox.showwarning("Non trouvé", "Aucune réservation avec ce nom.")
        except FileNotFoundError:
            messagebox.showwarning("Erreur", "Le fichier de réservation est introuvable.")

    def rechercher():
        nom = nom_entry.get()
        if not nom:
            messagebox.showerror("Erreur", "Veuillez entrer un nom pour rechercher.")
            return

        listbox.delete(0, tk.END)
        trouve = False
        try:
            with open("fichier.csv", "r", newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=";")
                for ligne in reader:
                    if ligne and nom.lower() in ligne[0].lower():
                        listbox.insert(tk.END, " | ".join(ligne))
                        trouve = True
            if not trouve:
                messagebox.showinfo("Résultat", "Aucune réservation trouvée pour ce nom.")
        except FileNotFoundError:
            messagebox.showwarning("Erreur", "Le fichier de réservation est introuvable.")

    def effacer():
        nom_entry.delete(0, tk.END)
        num_chambre.delete(0, tk.END)
        jours_entry.delete(0, tk.END)
        type_chambre.set("Simple")
        listbox.delete(0, tk.END)

    #  Boutons alignés 
    btn_frame = tk.Frame(frame, bg="#0c1b33")
    btn_frame.pack(pady=10)

    style_btn = {
        "bg": "#d4a857",
        "fg": "black",
        "font": ("Arial", 10, "bold"),
        "padx": 8,
        "pady": 5
    }

    tk.Button(btn_frame, text="Ajouter", command=reserver, **style_btn).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Afficher", command=afficher, **style_btn).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Supprimer", command=supprimer, **style_btn).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Effacer", command=effacer, **style_btn).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Rechercher", command=rechercher, **style_btn).pack(side="left", padx=5)

    retour = tk.Label(frame, text="⬅ Retour", bg="#0c1b33", fg="gold", cursor="hand2", font=("Arial", 11, "underline"))
    retour.pack(pady=(10, 0))
    retour.bind("<Button-1>", lambda e: afficher_connexion())

# Lancer l'app
afficher_connexion()
root.mainloop()

