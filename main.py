from config import Config
from formulaires import LoginForm
from singleton import *
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    DateField
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, request, session, g

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


class Utilisateur:
    def __init__(self, id, pseudo, mdp):
        self.id = id
        self.pseudo = pseudo
        self.mdp = mdp

#tableau contenant la liste des utilisateurs avec le droit d'acceder au site
db = DBSingleton.Instance()
users = db.fetchall_simple("SELECT id,login,mot_de_passe FROM utilisateur")
utilisateurs = []
for i in users:
    globals()["Utilisateur%s" % str(i[0])] = Utilisateur(id=i[0], pseudo=i[1], mdp=i[2])
    utilisateurs.append(eval("Utilisateur%s" % i[0]))


@app.before_request
def before_request():
    g.utilisateur = False
    if 'utilisateur_id' in session:
        utilisateur = [x for x in utilisateurs if x.id == session['utilisateur_id']]
        g.utilisateur = utilisateur[0]

@app.route('/', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        session.pop('utilisateur_id', None)
        pseudo = request.form['pseudo']
        mdp = request.form['mdp']

        utilisateur = [x for x in utilisateurs if x.pseudo == pseudo]
        if not utilisateur==[]:
            if utilisateur[0].mdp == mdp:
                session['utilisateur_id'] = utilisateur[0].id
                return redirect('/accueil')
            return redirect('/accueil')
    form = LoginForm()
    return render_template('index.html', form=form, title='connexion')


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
    valider = SubmitField('Valider')


@app.route('/menu-entreprises/<prospect>/<statut>/<recherche>', methods=['GET', 'POST'])
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


@app.route('/contact/<prospect>/<contact>')
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
@app.route('/changer-statut/<prospect>/<contact_id>')
def  changement_statut(prospect,contact_id):
    statut_actuel=Select("contact","statut","id",contact_id)[0]
    print(statut_actuel)
    if statut_actuel==0:
        update("contact","statut",(1,),"id",contact_id)
        return redirect("/menu-entreprises/"+prospect+"/actif/filtre-off")
    if  statut_actuel==1:
        update("contact","statut",(0,),"id",contact_id)
        return redirect("/menu-entreprises/"+prospect+"/inactif/filtre-off")
if __name__ == "__main__":
    app.run(debug=True)
