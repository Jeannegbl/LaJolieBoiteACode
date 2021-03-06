from config import Config
from formulaires import LoginForm
from singleton import *
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    DateField, EmailField, TelField, DecimalField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, request, session, g
from datetime import datetime, timedelta
from factures import *
import os

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv('.env')


class Utilisateur:
    def __init__(self, id, pseudo, mdp):
        self.id = id
        self.pseudo = pseudo
        self.mdp = mdp


# tableau contenant la liste des utilisateurs avec le droit d'acceder au site
db = DBSingleton.Instance()
users = db.fetchall_simple("SELECT id,login,mot_de_passe FROM utilisateur")
utilisateurs = []
for i in users:
    user = Utilisateur(id=i[0], pseudo=i[1], mdp=i[2])
    # globals()["Utilisateur%s" % str(i[0])] = Utilisateur(id=i[0], pseudo=i[1], mdp=i[2])
    utilisateurs.append(user)  # eval("Utilisateur%s" % i[0]))


@app.before_request
def before_request():
    g.utilisateur = False
    if 'utilisateur_id' in session:
        utilisateur = [x for x in utilisateurs if x.id == session['utilisateur_id']]
        g.utilisateur = utilisateur[0]  # get_user_from_db(session['pseudo'])


@app.route('/', methods=['GET', 'POST'])
def connexion():
    form = LoginForm()
    result = render_template('index.html', form=form, title='connexion')
    if request.method == 'POST':
        session.pop('utilisateur_id', None)
        pseudo = request.form['pseudo']
        mdp = request.form['mdp']
        utilisateur = [x for x in utilisateurs if x.pseudo == pseudo]

        # utilisateur = get_user_from_db(pseudo)
        session.permanent = False
        app.permanent_session_lifetime = timedelta(hours=1)
        if len(utilisateur):
            if utilisateur[0].mdp == mdp:
                session['utilisateur_id'] = utilisateur[0].id
                session['pseudo'] = utilisateur[0].pseudo
                instant = datetime.now()
                session['heure_connexion'] = instant
                result = redirect('/accueil')
    return result


@app.route('/deconnexion')
def deconnexion():
    del session['utilisateur_id']
    return redirect('/')


@app.route('/accueil')
def accueil():
    connexion_unique = DBSingleton.Instance()
    element = "SELECT prospect.nom, COUNT(facture.id) AS 'Nombre de facture' FROM `prospect` LEFT JOIN facture ON " \
              "facture.prospect_id = prospect.id GROUP BY prospect.nom ORDER BY prospect.nom ASC "
    prospects = connexion_unique.fetchall_simple(element)
    result = render_template('accueil.html', prospects=prospects)
    if not g.utilisateur:
        result = redirect('/')
    return result


class BarreDeRechercheFiltre(FlaskForm):
    filtreDefini = StringField("Filtrer les contacts", validators=[DataRequired()])
    valider = SubmitField('Rechercher')


@app.route('/menu-entreprises/<prospect>/<statut>/<recherche>', methods=['GET', 'POST'])
def prospect(prospect, statut, recherche):
    # filtre en fonction du statut
    if statut == "inactif":
        bool_statut = 0
    else:
        bool_statut = 1
    # filtre de recherche de nom/email
    if recherche == "filtre-off":
        sqlfiltre = ""
    else:
        sqlfiltre = "and (contact.`nom` LIKE '" + recherche + "%' or contact.`email` LIKE '" + recherche + \
                    "%' or contact.`prenom` LIKE '" + recherche + "%')"
    connexion_unique = DBSingleton.Instance()
    sql = "SELECT contact.*, COUNT(commentaire.contact_id) AS 'Nombre de commentaire' FROM `contact` LEFT JOIN " \
          "commentaire ON commentaire.contact_id = contact.id JOIN prospect ON prospect.id = contact.prospect_id " \
          "WHERE prospect.nom = %s AND statut = '" + str(bool_statut) + "' " + sqlfiltre + " GROUP BY contact.email"
    params: tuple = (prospect,)
    contacts = connexion_unique.query(sql, params)
    element_2 = "SELECT prospect.numero_siret, prospect.adresse_postale, prospect.code_postal, prospect.ville, " \
                "prospect.description, prospect.url FROM `prospect` WHERE prospect.nom = '%s' " % prospect
    info_prospect = connexion_unique.fetchall_simple(element_2)
    activiter = bool_statut
    filtre = BarreDeRechercheFiltre()
    result = render_template('prospect.html', contacts=contacts, nom_prospect=prospect, info_prospect=info_prospect,
                             activiter=activiter, barrederecherche=filtre,style_additionnel="style=display:block;")
    if not g.utilisateur:
        result = redirect('/')
    if filtre.valider.data == True:
        result = redirect("/menu-entreprises/" + prospect + "/" + statut + "/" + filtre.filtreDefini.data)
    return result


@app.route('/contact/<prospect>/<contact>')
def contact(contact, prospect):
    connexion_unique = DBSingleton.Instance()
    element = "SELECT contact.*, COUNT(commentaire.contact_id) AS 'Nombre de commentaire' FROM `contact` LEFT JOIN " \
              "commentaire ON commentaire.contact_id = contact.id JOIN prospect ON prospect.id = contact.prospect_id " \
              "WHERE prospect.nom = '%s' AND statut = '0' GROUP BY contact.nom" % prospect
    contacts = connexion_unique.fetchall_simple(element)
    element_2 = "SELECT commentaire.description, commentaire.date_creation, utilisateur.login FROM `contact`JOIN " \
                "commentaire ON commentaire.contact_id = contact.id JOIN utilisateur ON utilisateur.id = " \
                "commentaire.utilisateur_id WHERE contact.id = '%s' ORDER BY date_creation DESC LIMIT 1" % contact
    commentaire = connexion_unique.fetchall_simple(element_2)
    element_3 = "SELECT commentaire.description, commentaire.date_creation, utilisateur.login FROM `contact`JOIN " \
                "commentaire ON commentaire.contact_id = contact.id JOIN utilisateur ON utilisateur.id = " \
                "commentaire.utilisateur_id WHERE contact.id = '%s' ORDER BY date_creation DESC LIMIT 100 OFFSET 1 " \
                % contact
    liste_commentaires = connexion_unique.fetchall_simple(element_3)
    result = render_template('contact.html', contacts=contacts, nom_prospect=prospect, contact=contact,
                             commentaire=commentaire, liste_commentaires=liste_commentaires)
    if not g.utilisateur:
        result = redirect('/')

    return result


@app.route('/changer-statut/<prospect>/<contact_id>')
def changement_statut(prospect, contact_id):
    if not g.utilisateur:
        result = redirect('/')
    statut_actuel = select("contact", "statut", "id", contact_id)[0][0]
    if statut_actuel == 0:
        update("contact", "statut", (1,), "id", contact_id)
        result = redirect("/menu-entreprises/" + prospect + "/actif/filtre-off")
    if statut_actuel == 1:
        update("contact", "statut", (0,), "id", contact_id)
        result = redirect("/menu-entreprises/" + prospect + "/inactif/filtre-off")
    return result





# @app.route('/generer_facture/<prospect_nom>/<contact_id>', methods=['GET', 'POST'])
def genration_factures(prospect_nom, contact_id):
    result = render_template("apercufacture.html", )
    if not g.utilisateur:
        result = redirect('/')
    formFacture = FormulaireFacturation()
    if formFacture.valider.data == True:
        prospect_id = select("prospect", "id", "nom", prospect_nom)[0][0]
        entreprise_id = os.environ.get('entreprise_id')
        date = str(datetime.now())[:-7]

        nombre_factures = 0
        dir = os.environ.get("chemin_complet_dossier_factures")
        for path in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, path)):
                nombre_factures += 1
        params: tuple = (
            nombre_factures + 1, date, formFacture.montant_facture.data, contact_id, prospect_id, entreprise_id)
        insert("facture", "numero_facture,date_emission,montant,contact_id,prospect_id,entreprise_id", params)
        facture_id = select("facture", "id", "date_emission", date)[0][0]

        entreprise = Entreprise(os.environ.get('entreprise_id'))
        prospect = Prospect(prospect_id)
        contact = Contact(contact_id)
        details_facture = Details_facture(facture_id)
        facture = Facture(entreprise, prospect, contact, details_facture)
        facture.generate()
        nom_facture = facture.nomFacture
        result = redirect("/apercu_facture/" + nom_facture)
    return result
@app.route('/factures/<nom_prospect>', methods=['GET', 'POST'])
def factures_prospect(nom_prospect):
    if not g.utilisateur:
        result= redirect('/')
    else:
        liste_url = []
        formFacture = FormulaireFacturation()
        prospect_id=select("prospect","id","nom",nom_prospect)[0][0]
        contacts_ids=select("contact", "id", "prospect_id", prospect_id)
        for contact_id in contacts_ids:
            i = 0
            for _ in select("facture", "id", "contact_id", contact_id[0]):
                details_facture = Details_facture(select("facture", "id", "contact_id", contact_id[0])[i][0])
                entreprise = Entreprise(os.environ.get('entreprise_id'))
                prospect = Prospect(select("prospect", "id", "nom", nom_prospect)[0][0])
                contact = Contact(contact_id[0])
                facture = Facture(entreprise, prospect, contact, details_facture)
                liste_url.append(os.environ.get("url_dossier_factures") + facture.nomFacture + ".pdf")
                i += 1
        result = render_template("apercufacture.html", effaceur="style=display:none;",formFacture=formFacture, liste_url=liste_url,nom_prospect=nom_prospect,)
    return result
class FormulaireFacturation(FlaskForm):
    montant_facture = IntegerField("Envoyer une facture a ce contact", validators=[DataRequired()])
    valider = SubmitField('Valider')

@app.route('/apercu_factures/<nom_prospect>/<id_contact>', methods=['GET', 'POST'])
def apercu_factures(nom_prospect, id_contact):
    if not g.utilisateur:
        result= redirect('/')
    else:
        i = 0
        liste_url = []
        formFacture = FormulaireFacturation()
        for _ in select("facture", "id", "contact_id", id_contact):
            details_facture = Details_facture(select("facture", "id", "contact_id", id_contact)[i][0])
            entreprise = Entreprise(os.environ.get('entreprise_id'))
            prospect = Prospect(select("prospect", "id", "nom", nom_prospect)[0][0])
            contact = Contact(id_contact)
            facture = Facture(entreprise, prospect, contact, details_facture)
            liste_url.append(os.environ.get("url_dossier_factures") + facture.nomFacture + ".pdf")
            i += 1

        result = render_template("apercufacture.html", formFacture=formFacture, liste_url=liste_url)
        if formFacture.valider.data == True:
            result=redirect(f"/creation_facture/{nom_prospect}/{id_contact}/{formFacture.montant_facture.data}")
    return result


@app.route('/creation_facture/<nom_prospect>/<id_contact>/<montant_facture>', methods=['GET', 'POST'])
def creation_facture(nom_prospect, id_contact,montant_facture):
    if not g.utilisateur:
        result = redirect('/')
    else:
            prospect_id = select("prospect", "id", "nom", nom_prospect)[0][0]
            entreprise_id = os.environ.get('entreprise_id')
            date = str(datetime.now())[:-7]
            nombre_factures = 0
            dir = os.environ.get("chemin_complet_dossier_factures")
            for path in os.listdir(dir):
                if os.path.isfile(os.path.join(dir, path)):
                    nombre_factures += 1
            params: tuple = (
                nombre_factures + 1, date, montant_facture, id_contact, prospect_id, entreprise_id)
            insert("facture", "numero_facture,date_emission,montant,contact_id,prospect_id,entreprise_id", params)
            facture_id = select("facture", "id", "date_emission", date)[0][0]

            entreprise = Entreprise(os.environ.get('entreprise_id'))
            prospect = Prospect(prospect_id)
            contact = Contact(id_contact)
            details_facture = Details_facture(facture_id)
            facture = Facture(entreprise, prospect, contact, details_facture)
            facture.generate()
            result=redirect(f"/apercu_factures/{nom_prospect}/{id_contact}")
    return result


@app.route('/effacer-prospect/<prospect>')
def effacer_prospect(prospect):
    result = redirect("/accueil")
    if not g.utilisateur:
        result = redirect('/')
    id_prospect = select("prospect", "id", "nom", prospect)[0][0]
    delete("prospect", "id", id_prospect)
    return result


@app.route('/ajouter-prospect', methods=['GET', 'POST'])
def ajouter_prospect():
    class Ajouterprospect(FlaskForm):
        nom = StringField('nom', validators=[DataRequired()])
        siret = DecimalField('siret', validators=[DataRequired()])
        adresse = StringField('adresse', validators=[DataRequired()])
        codepostal = DecimalField('codepostal', validators=[DataRequired()])
        ville = StringField('ville', validators=[DataRequired()])
        description = TextAreaField('description')
        url = TextAreaField('url')
    form = Ajouterprospect()
    result = render_template('ajouter-prospect.html', form=form)
    if not g.utilisateur:
        result = redirect('/')
    if form.validate_on_submit():
        nom = request.form['nom']
        siret = request.form['siret']
        adresse = request.form['adresse']
        codepostal = request.form['codepostal']
        ville = request.form['ville']
        description = request.form['description']
        url = request.form['url']
        params: tuple = (nom, siret, adresse, codepostal, ville, description, url)
        insert("prospect", "nom, numero_siret, adresse_postale, code_postal, ville, description, url", params)
        result = redirect("/accueil")
    return result


@app.route('/ajouter-contact/<prospect>', methods=['GET', 'POST'])
def ajouter_contact(prospect):
    class Ajoutercontact(FlaskForm):
        nom = StringField('nom', validators=[DataRequired()])
        prenom = StringField('prenom', validators=[DataRequired()])
        email = EmailField('email', validators=[DataRequired()])
        poste = StringField('poste')
        telephone = DecimalField('telephone')

    form = Ajoutercontact()
    result = render_template('ajouter-contact.html', form=form)
    if not g.utilisateur:
        result = redirect('/')

    if form.validate_on_submit():
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        poste = request.form['poste']
        telephone = request.form['telephone']
        statut = '1'
        id_prospect = select("prospect", "id", "nom", prospect)[0][0]
        params: tuple = (nom, prenom, email, poste, telephone, statut, id_prospect)
        insert("contact", "nom, prenom, email, poste, telephone, statut, prospect_id", params)
        result = redirect("/menu-entreprises/" + prospect + "/actif/filtre-off")
    return result

@app.route('/ajouter-commentaire/<prospect>/<id_contact>', methods=['GET', 'POST'])
def ajouter_commentaire(prospect, id_contact):
    class Ajoutercommentaire(FlaskForm):
        commentaire = TextAreaField('commentaire', validators=[DataRequired()])
    form = Ajoutercommentaire()
    result = render_template('ajouter-commentaire.html', form=form)
    if not g.utilisateur:
        result = redirect('/')

    if form.validate_on_submit():
        commentaire = request.form['commentaire']
        contact = id_contact
        utilisateur = session['utilisateur_id']
        params: tuple = (utilisateur, contact, commentaire)
        insert("commentaire", "utilisateur_id, contact_id, description", params)
        result = redirect("/contact/" + prospect + "/" + id_contact)
    return result


if __name__ == "__main__":
    app.run(debug=True)
