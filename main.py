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


# pythoncom.CoInitialize()
class Utilisateur:
    def __init__(self, id, pseudo, mdp):
        self.id = id
        self.pseudo = pseudo
        self.mdp = mdp



def get_user_from_db(pseudo):
    db = DBSingleton.Instance()
    users = db.fetchall_simple("SELECT id,login,mot_de_passe as mdp FROM utilisateur WHERE login = '%s'" % pseudo)
    return Utilisateur(*users[0]) if len(users) else None


@app.before_request
def before_request():
    g.utilisateur = False
    if 'utilisateur_id' in session:
        g.utilisateur = get_user_from_db(session['pseudo'])


@app.route('/', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        session.pop('utilisateur_id', None)
        pseudo = request.form['pseudo']
        mdp = request.form['mdp']

        utilisateur = get_user_from_db(pseudo)
        session.permanent = False
        app.permanent_session_lifetime = timedelta(hours=1)
        if utilisateur:
            print(utilisateur)
            if utilisateur.mdp == mdp:
                session['utilisateur_id'] = utilisateur.id
                session['pseudo'] = utilisateur.pseudo
                instant = datetime.now()
                session['heure_connexion'] = instant
                return redirect('/accueil')
    form = LoginForm()
    return render_template('index.html', form=form, title='connexion')


@app.route('/deconnexion')
def deconnexion():
    del session['utilisateur_id']
    if 'heure_expiration' in session :
        del session['heure_expiration']
    return redirect('/')


@app.route('/accueil')
def accueil():
    if not g.utilisateur:
        return redirect('/')
    connexion_unique = DBSingleton.Instance()
    element = "SELECT prospect.nom, COUNT(facture.id) AS 'Nombre de facture' FROM `prospect` LEFT JOIN facture ON facture.prospect_id = prospect.id GROUP BY prospect.nom ORDER BY prospect.nom ASC"
    prospects = connexion_unique.fetchall_simple(element)
    return render_template('accueil.html', prospects=prospects)


class BarreDeRechercheFiltre(FlaskForm):
    filtreDefini = StringField("Filtrer les contacts", validators=[DataRequired()])
    valider = SubmitField('Rechercher')


@app.route('/menu-entreprises/<prospect>/<statut>/<recherche>', methods=['GET', 'POST'])
def prospect(prospect, statut, recherche):
    if not g.utilisateur:
        return redirect('/')
    filtre = BarreDeRechercheFiltre()
    if filtre.valider.data == True:
        return redirect("/menu-entreprises/" + prospect + "/" + statut + "/" + filtre.filtreDefini.data)
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


@app.route('/contact/<prospect>/<contact>')
def contact(contact, prospect):
    if not g.utilisateur:
        return redirect('/')
    connexion_unique = DBSingleton.Instance()
    element = "SELECT contact.*, COUNT(commentaire.contact_id) AS 'Nombre de commentaire' FROM `contact` LEFT JOIN commentaire ON commentaire.contact_id = contact.id JOIN prospect ON prospect.id = contact.prospect_id WHERE prospect.nom = '%s' AND statut = '0' GROUP BY contact.nom" % prospect
    contacts = connexion_unique.fetchall_simple(element)
    element_2 = "SELECT commentaire.description, commentaire.date_creation, utilisateur.login FROM `contact`JOIN commentaire ON commentaire.contact_id = contact.id JOIN utilisateur ON utilisateur.id = commentaire.utilisateur_id WHERE contact.id = '%s' ORDER BY date_creation DESC LIMIT 1" % contact
    commentaire = connexion_unique.fetchall_simple(element_2)
    element_3 = "SELECT commentaire.description, commentaire.date_creation, utilisateur.login FROM `contact`JOIN commentaire ON commentaire.contact_id = contact.id JOIN utilisateur ON utilisateur.id = commentaire.utilisateur_id WHERE contact.id = '%s' ORDER BY date_creation DESC LIMIT 100 OFFSET 1 " % contact
    liste_commentaires = connexion_unique.fetchall_simple(element_3)
    return render_template('contact.html', contacts=contacts, nom_prospect=prospect, contact=contact,
                           commentaire=commentaire, liste_commentaires=liste_commentaires)


@app.route('/changer-statut/<prospect>/<contact_id>')
def changement_statut(prospect, contact_id):
    if not g.utilisateur:
        return redirect('/')
    statut_actuel = select("contact", "statut", "id", contact_id)[0][0]
    if statut_actuel == 0:
        update("contact", "statut", (1,), "id", contact_id)
        return redirect("/menu-entreprises/" + prospect + "/actif/filtre-off")
    if statut_actuel == 1:
        update("contact", "statut", (0,), "id", contact_id)
        return redirect("/menu-entreprises/" + prospect + "/inactif/filtre-off")


class FormulaireFacturation(FlaskForm):
    montant_facture = IntegerField("Montant de la facture", validators=[DataRequired()])
    valider = SubmitField('Valider')


@app.route('/generer_facture/<prospect_nom>/<contact_id>', methods=['GET', 'POST'])
def genration_factures(prospect_nom, contact_id):
    if not g.utilisateur:
        return redirect('/')
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
        return redirect("/apercu_facture/" + nom_facture)
    return render_template("facturemontant.html", formFacture=formFacture)


@app.route('/apercu_factures/<nom_prospect>/<id_contact>', methods=['GET', 'POST'])
def apercu_factures(nom_prospect, id_contact):
    if not g.utilisateur:
        return redirect('/')
    listeFactures=[]
    i=0
    for _ in select("facture", "id", "contact_id", id_contact):
        details_facture = Details_facture(select("facture", "id", "contact_id", id_contact)[i][0])
        entreprise = Entreprise(os.environ.get('entreprise_id'))
        prospect = Prospect(select("prospect", "id", "nom", nom_prospect)[0][0])
        contact = Contact(id_contact)
        facture=Facture(entreprise,prospect,contact,details_facture)
        listeFactures.append(facture.nomFacture)
        print(listeFactures, i)
        print(select("facture", "id", "contact_id", id_contact)[0])
        i+=1



@app.route('/apercu_facture/<nom_facture>', methods=['GET', 'POST'])
def apercu_facture(nom_facture):
    if not g.utilisateur:
        return redirect('/')
    urlpdf = os.environ.get("url_dossier_factures") + nom_facture + ".pdf"
    return render_template("apercufacture.html", urlpdf=urlpdf)


@app.route('/effacer-prospect/<prospect>')
def effacer_prospect(prospect):
    if not g.utilisateur:
        return redirect('/')
    id_prospect = select("prospect", "id", "nom", prospect)[0][0]
    delete("prospect", "id", id_prospect)
    return redirect("/accueil")


@app.route('/ajouter-prospect', methods=['GET', 'POST'])
def ajouter_prospect():
    if not g.utilisateur:
        return redirect('/')
    class Ajouterprospect(FlaskForm):
        nom = StringField('nom', validators=[DataRequired()])
        siret = DecimalField('siret', validators=[DataRequired()])
        adresse = StringField('adresse', validators=[DataRequired()])
        codepostal = DecimalField('codepostal', validators=[DataRequired()])
        ville = StringField('ville', validators=[DataRequired()])
        description = TextAreaField('description')
        url = TextAreaField('url')

    form = Ajouterprospect()
    if form.validate_on_submit():
        nom = request.form['nom']
        siret = request.form['siret']
        adresse = request.form['adresse']
        codepostal = request.form['codepostal']
        ville = request.form['ville']
        description = request.form['description']
        url = request.form['url']
        params: tuple = (nom, siret, adresse, codepostal, ville, description, url)
        Insert("prospect", "nom, numero_siret, adresse_postale, code_postal, ville, description, url", params)
        return redirect("/accueil")
    return render_template('ajouter-prospect.html', form=form)


@app.route('/ajouter-contact/<prospect>', methods=['GET', 'POST'])
def ajouter_contact(prospect):
    if not g.utilisateur:
        return redirect('/')
    class Ajoutercontact(FlaskForm):
        nom = StringField('nom', validators=[DataRequired()])
        prenom = StringField('prenom', validators=[DataRequired()])
        email = EmailField('email', validators=[DataRequired()])
        poste = StringField('poste')
        telephone = TelField('telephone')

    form = Ajoutercontact()
    if form.validate_on_submit():
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        poste = request.form['poste']
        telephone = request.form['telephone']
        statut = '1'
        id_prospect = select("prospect", "id", "nom", prospect)[0][0]
        params: tuple = (nom, prenom, email, poste, telephone, statut, id_prospect)
        Insert("contact", "nom, prenom, email, poste, telephone, statut, prospect_id", params)
        return redirect("/menu-entreprises/" + prospect + "/actif/filtre-off")
    return render_template('ajouter-contact.html', form=form)


@app.route('/ajouter-commentaire/<prospect>/<id_contact>', methods=['GET', 'POST'])
def ajouter_commentaire(prospect, id_contact):
    if not g.utilisateur:
        return redirect('/')
    class Ajoutercommentaire(FlaskForm):
        commentaire = TextAreaField('commentaire', validators=[DataRequired()])

    form = Ajoutercommentaire()
    if form.validate_on_submit():
        commentaire = request.form['commentaire']
        contact = id_contact
        utilisateur = session['utilisateur_id']
        params: tuple = (utilisateur, contact, commentaire)
        Insert("commentaire", "utilisateur_id, contact_id, description", params)
        return redirect("/contact/" + prospect + "/" + id_contact)
    return render_template('ajouter-commentaire.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
