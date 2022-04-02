from models import *
from flask import render_template, Flask, session
from config import Config
from formulaires import RegisterForm
from singleton import *


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['get', 'post'])
def index():
    form = RegisterForm()
    return render_template('connexion.html', form=form, title='connexion')


@app.route('/accueil')
def accueil():
    connexion_unique = DBSingleton.Instance()
    element = "SELECT prospect.nom, COUNT(facture.id) AS 'Nombre de facture' FROM `prospect` LEFT JOIN facture ON facture.prospect_id = prospect.id GROUP BY prospect.nom ORDER BY prospect.nom ASC"
    prospects = connexion_unique.fetchall_simple(element)
    return render_template('accueil.html', prospects=prospects)

@app.route('/<prospect>')
def prospect(prospect):
    connexion_unique = DBSingleton.Instance()
    element = "SELECT contact.*, COUNT(commentaire.contact_id) AS 'Nombre de commentaire' FROM `contact` LEFT JOIN commentaire ON commentaire.contact_id = contact.id JOIN prospect ON prospect.id = contact.prospect_id WHERE prospect.nom = '%s' AND statut = '1' GROUP BY contact.nom" % prospect
    contacts = connexion_unique.fetchall_simple(element)
    element_2 = "SELECT prospect.numero_siret, prospect.adresse_postale, prospect.code_postal, prospect.ville, prospect.description, prospect.url FROM `prospect` WHERE prospect.nom = '%s' " % prospect
    info_prospect = connexion_unique.fetchall_simple(element_2)
    activiter = 1
    return render_template('prospect.html', contacts=contacts, nom_prospect=prospect, info_prospect=info_prospect, activiter=activiter)

@app.route('/<prospect>/inactif')
def inactif(prospect):
    connexion_unique = DBSingleton.Instance()
    element = "SELECT contact.*, COUNT(commentaire.contact_id) AS 'Nombre de commentaire' FROM `contact` LEFT JOIN commentaire ON commentaire.contact_id = contact.id JOIN prospect ON prospect.id = contact.prospect_id WHERE prospect.nom = '%s' AND statut = '0' GROUP BY contact.nom" % prospect
    contacts = connexion_unique.fetchall_simple(element)
    element_2 = "SELECT prospect.numero_siret, prospect.adresse_postale, prospect.code_postal, prospect.ville, prospect.description, prospect.url FROM `prospect` WHERE prospect.nom = '%s' " % prospect
    info_prospect = connexion_unique.fetchall_simple(element_2)
    activiter = 0
    session['prospect'] = prospect
    return render_template('prospect.html', contacts=contacts, nom_prospect=prospect, info_prospect=info_prospect, activiter=activiter)

@app.route('/<prospect>/contact/<contact>')
def contact(contact,prospect):
    connexion_unique = DBSingleton.Instance()
    element = "SELECT contact.*, COUNT(commentaire.contact_id) AS 'Nombre de commentaire' FROM `contact` LEFT JOIN commentaire ON commentaire.contact_id = contact.id JOIN prospect ON prospect.id = contact.prospect_id WHERE prospect.nom = '%s' AND statut = '0' GROUP BY contact.nom" % prospect
    contacts = connexion_unique.fetchall_simple(element)
    element_2 = "SELECT commentaire.description, commentaire.date_creation, utilisateur.login FROM `contact`JOIN commentaire ON commentaire.contact_id = contact.id JOIN utilisateur ON utilisateur.id = commentaire.utilisateur_id WHERE contact.nom = '%s' ORDER BY date_creation DESC LIMIT 1" % contact
    commentaire = connexion_unique.fetchall_simple(element_2)
    element_3 = "SELECT commentaire.description, commentaire.date_creation, utilisateur.login FROM `contact`JOIN commentaire ON commentaire.contact_id = contact.id JOIN utilisateur ON utilisateur.id = commentaire.utilisateur_id WHERE contact.nom = '%s' ORDER BY date_creation DESC LIMIT 100 OFFSET 1 "  % contact
    liste_commentaires = connexion_unique.fetchall_simple(element_3)
    return render_template('contact.html', contacts=contacts, nom_prospect=prospect, contact=contact, commentaire=commentaire, liste_commentaires=liste_commentaires)



if __name__ == "__main__":
    app.run(debug=True)
