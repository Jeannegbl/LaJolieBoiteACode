import datetime
from singleton import DBSingleton
from docxtpl import DocxTemplate


if __name__ == "__main__":
    db = DBSingleton.Instance()
    def Select(table,col,id):
        sql="SELECT %s from %s WHERE id=%s"
        params:tuple=(col,table,id)
        db.query(sql,params)
        return db.result[0]


    template_values = {}
    document = DocxTemplate("Factures/template/template.docx")

class information_entreprise():
    nom =
    rue =
    adresse =
    code_postal =
    ville =
    cedex =
    SIREN =
    tel =
    email =
    IBAN =

class information_prospect():
    nom =
    adresse =
    code_postal =
    ville =

class information_contact():
    nom =

class Facture():
    def __init__(self, information_entreprise: information_entreprise, information_prospect: information_prospect, information_contact: information_contact, siren, email:str):
        self.rue = emmeteur.rue
        self.ville = ville


    def generate(self):
        document.render(template_values)
        document.save("Factures/facture_" + idFacture + ".docx")


    tel = "06332925"
    template_values["tel"] = tel

    email = "Gillian@charra"
    template_values["email"] = email


    IBAN = "3090986307245678"
    template_values["IBAN"] = IBAN

    prenomClient = "Gillian"
    template_values["prenom"] = prenomClient

    nomClient = "Charra"
    template_values["nom"] = nomClient

    idFacture = "452AORT286"
    template_values["idfacture"] = idFacture

    montant = "400"
    template_values["montant"] = montant

    date = str(datetime.datetime.now())
    template_values["date"] = date

