from singleton import select


class Entreprise:
    def __init__(self, id):
        element = select('entreprise', 'nom, adresse_postale, code_postal, ville, cedex, numero_siren, telephone, '
                                       'email, IBAN',"id", id)[0]
        self.nom_e = element[0]
        self.adresse_e = element[1]
        self.code_postal_e = str(element[2])
        self.ville_e = element[3]
        self.cedex_e = str(element[4])
        self.SIREN_e = element[5]
        self.tel_e = str(element[6])
        self.email_e = element[7]
        self.IBAN_e = element[8]


class Prospect:
    def __init__(self, id):
        element = select('prospect', 'nom, adresse_postale, code_postal, ville',"id", id)[0]
        self.nom_p = element[0]
        self.adresse_p = element[1]
        self.code_postal_p = str(element[2])
        self.ville_p = element[3]


class Contact:
    def __init__(self, id):
        element = select('contact', 'nom',"id", id)[0]
        self.nom_c = element[0]


class Details_facture:
    def __init__(self, id):
        element = select('facture','numero_facture, date_emission, montant',"id", id)[0]
        self.numero_f = str(element[0])
        charADegager = [":", " "]
        dateAImplementer = str(element[1])
        for i in range(len(charADegager)):
            dateAImplementer = dateAImplementer.replace(charADegager[i], "")
        self.date_emission_f = dateAImplementer
        self.montant_f = str(element[2])


class Prospectaccueil:
    def __init__(self, id):
        element = select( 'prospect','nom, numero_siret, adresse_postale, code_postal, ville, description, url',"id", id)[0]
        self.nom_p = element[0]
        self.siret_p = str(element[1])
        self.adresse_p = element[2]
        self.code_postal_p = str(element[3])
        self.ville_p = element[4]
        self.desc_p = element[5]
        self.url_p = element[6]
