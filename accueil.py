from singleton import Select
from flask import render_template, Flask, session, redirect, request, url_for

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


class Prospect:
    def __init__(self, id):
        element = Select('nom, numero_siret, adresse_postale, code_postal, ville, description, url', 'prospect', id)
        self.nom_p = element[0]
        self.siret_p = element[1]
        self.adresse_p = element[2]
        self.code_postal_p = str(element[3])
        self.ville_p = element[4]
        self.desc_p = element[5]
        self.url_p = element[6]



@app.route('/accueil')
def index():
    prospect = Prospect(1)
    return render_template('accueil.html', prospect=prospect)




if __name__ == '__main__':
    app.run(debug=True)