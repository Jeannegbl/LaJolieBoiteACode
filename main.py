from models import *
from config import Config
from formulaires import RegisterForm
from werkzeug.utils import redirect
from singleton import *
from flask import render_template, Flask, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    DateField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterForm()
    return render_template('connexion.html', form=form, title='connexion')


@app.route('/accueil')
def accueil():
    connexion_unique = DBSingleton.Instance()
    element = "SELECT prospect.nom, COUNT(facture.id) AS 'Nombre de facture' FROM `prospect` LEFT JOIN facture ON facture.prospect_id = prospect.id GROUP BY prospect.nom ORDER BY prospect.nom ASC"
    prospects = connexion_unique.fetchall_simple(element)
    return render_template('accueil.html', prospects=prospects)


class BarreDeRechercheFiltre(FlaskForm):
    filtreDefini = StringField("Filtrer les contacts", validators=[DataRequired()])
    valider = SubmitField('Valider')


@app.route('/<prospect>/<statut>/<recherche>', methods=['GET', 'POST'])
def prospect(prospect, statut, recherche):
    filtre = BarreDeRechercheFiltre()
    if filtre.valider.data == True:
        return redirect("/" + prospect + "/" + statut + "/" + filtre.filtreDefini.data)
    # filtre en fonction du statut
    if statut == "inactif":
        bool_statut = 0
    else:
        bool_statut = 1
    # filtre de recherche de nom/email
    if recherche == "filtre-off":
        sqlfiltre = ""
    else:
        sqlfiltre = "and (contact.`nom` LIKE '" + recherche + "%' or contact.`email` LIKE '" + recherche + "%' or contact.`prenom` LIKE '" + recherche + "%')"
    connexion_unique = DBSingleton.Instance()
    sql = "SELECT contact.*, COUNT(commentaire.contact_id) AS 'Nombre de commentaire' FROM `contact` LEFT JOIN " \
          "commentaire ON commentaire.contact_id = contact.id JOIN prospect ON prospect.id = contact.prospect_id " \
          "WHERE prospect.nom = %s AND statut = '" + str(bool_statut) + "' " + sqlfiltre + " GROUP BY contact.nom"
    params: tuple = (prospect,)
    contacts = connexion_unique.query(sql, params)
    element_2 = "SELECT prospect.numero_siret, prospect.adresse_postale, prospect.code_postal, prospect.ville, " \
                "prospect.description, prospect.url FROM `prospect` WHERE prospect.nom = '%s' " % prospect
    info_prospect = connexion_unique.fetchall_simple(element_2)
    activiter = bool_statut
    return render_template('prospect.html', contacts=contacts, nom_prospect=prospect, info_prospect=info_prospect,
                           activiter=activiter, barrederecherche=filtre)


@app.route('/<prospect>/contact/<contact>')
def contact(contact, prospect):
    connexion_unique = DBSingleton.Instance()
    element = "SELECT contact.*, COUNT(commentaire.contact_id) AS 'Nombre de commentaire' FROM `contact` LEFT JOIN commentaire ON commentaire.contact_id = contact.id JOIN prospect ON prospect.id = contact.prospect_id WHERE prospect.nom = '%s' AND statut = '0' GROUP BY contact.nom" % prospect
    contacts = connexion_unique.fetchall_simple(element)
    element_2 = "SELECT commentaire.description, commentaire.date_creation, utilisateur.login FROM `contact`JOIN commentaire ON commentaire.contact_id = contact.id JOIN utilisateur ON utilisateur.id = commentaire.utilisateur_id WHERE contact.nom = '%s' ORDER BY date_creation DESC LIMIT 1" % contact
    commentaire = connexion_unique.fetchall_simple(element_2)
    element_3 = "SELECT commentaire.description, commentaire.date_creation, utilisateur.login FROM `contact`JOIN commentaire ON commentaire.contact_id = contact.id JOIN utilisateur ON utilisateur.id = commentaire.utilisateur_id WHERE contact.nom = '%s' ORDER BY date_creation DESC LIMIT 100 OFFSET 1 " % contact
    liste_commentaires = connexion_unique.fetchall_simple(element_3)
    return render_template('contact.html', contacts=contacts, nom_prospect=prospect, contact=contact,
                           commentaire=commentaire, liste_commentaires=liste_commentaires)


if __name__ == "__main__":
    app.run(debug=True)
