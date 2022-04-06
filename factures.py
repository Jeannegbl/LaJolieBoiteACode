from docxtpl import DocxTemplate
from models import *
from docx2pdf import convert
import pythoncom
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv('.env')



class Facture:
    def __init__(self, entreprise: Entreprise, prospect: Prospect, contact: Contact, details_facture: Details_facture):
        self.entreprise = entreprise
        self.prospect = prospect
        self.contact = contact
        self.details_facture = details_facture
        self.nomFacture="facture_" + self.details_facture.numero_f +"_"+ self.details_facture.date_emission_f

    def generate(self):

        pythoncom.CoInitialize()
        document = DocxTemplate("Factures/template/template.docx")
        template_values = {
            'nom_e': self.entreprise.nom_e,
            'adresse_e': self.entreprise.adresse_e,
            'code_postal_e': self.entreprise.code_postal_e,
            'ville_e': self.entreprise.ville_e,
            'cedex_e': self.entreprise.cedex_e,
            'siren_e': self.entreprise.SIREN_e,
            'tel_e': self.entreprise.tel_e,
            'email_e': self.entreprise.email_e,
            'iban_e': self.entreprise.IBAN_e,
            'nom_p': self.prospect.nom_p,
            'nom_c': self.contact.nom_c,
            'adresse_p': self.prospect.adresse_p,
            'code_postal_p': self.prospect.code_postal_p,
            'ville_p': self.prospect.ville_p,
            'numero_f': self.details_facture.numero_f,
            'date_f': self.details_facture.date_emission_f,
            'montant_f': str(self.details_facture.montant_f)
        }
        self.nomFacture="facture_" + self.details_facture.numero_f +"_"+ self.details_facture.date_emission_f
        document.render(template_values)
        print(os.environ.get("chemin_complet_dossier_factures")+self.nomFacture +".docx")
        document.save(os.environ.get("chemin_complet_dossier_factures")+self.nomFacture+".docx")
        convert (os.environ.get("chemin_complet_dossier_factures")+self.nomFacture +".docx")

if __name__ == "__main__":

    LaJolieBoiteACode = Entreprise(1)
    Prospect_test = Prospect(1)
    Contact_test = Contact(1)
    Details_facture_test = Details_facture(1)
    LaFacture = Facture(LaJolieBoiteACode, Prospect_test, Contact_test, Details_facture_test)
    LaFacture.generate()