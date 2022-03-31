from singleton import Select


class Entreprise:
    def __init__(self, id):
        element = Select('nom, adresse_postale, code_postal, ville, cedex, numero_siren, telephone, email, IBAN',
                         'entreprise', id)
        self.nom_e = element['nom']
        self.adresse_e = element['adresse_postale']
        self.code_postal_e = element['code_postal']
        self.ville_e = element['ville']
        self.cedex_e = element['cedex']
        self.SIREN_e = element['numero_siren']
        self.tel_e = element['telephone']
        self.email_e = element['email']
        self.IBAN_e = element['IBAN']


class Prospect:
    def __init__(self, id):
        element = Select('nom, adresse_postale, code_postal, ville', 'prospect', id)
        self.nom_p = element['nom']
        self.adresse_p = element['adresse_postale']
        self.code_postal_p = element['code_postal']
        self.ville_p = element['ville']


class Contact:
    def __init__(self, id):
        element = Select('nom', 'contact', id)
        self.nom_c = element['nom']


class Details_facture:
    def __init__(self, id):
        element = Select('numero_facture, date_emission, montant', 'facture', id)
        self.numero_f = element['numero_facture']
        self.date_emission_f = element['date_emission']
        self.montant_f = element['montant']
