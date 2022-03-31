from docxtpl import DocxTemplate
import datetime
from singleton import DBSingleton
if __name__ == "__main__":
    db = DBSingleton.Instance()
    def Select(table,col,id):
        sql="SELECT %s from %s WHERE id=%s"
        params:tuple=(col,table,id)
        db.query(sql,params)
        return db.result[0]


    template_values = {}
    document = DocxTemplate("Factures/template/template.docx")


    rue = "13 Rue fernand robert"
    template_values["rue"] = rue

    ville = "35000 Rennes France"
    template_values["ville"] = ville

    siret = "2309709863"
    template_values["siret"] = siret


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

    document.render(template_values)
    document.save("Factures/facture_"+idFacture+".docx")