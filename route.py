from flask import render_template, Flask
from models import Prospectaccueil
from config import Config
from formulaires import RegisterForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['get', 'post'])
def index():
    form = RegisterForm()
    if form.validate_on_submit():
        print(f'Pseudo:{form.pseudo.data}')
    return render_template('connexion.html', form=form, title='connexion')

@app.route('/accueil')
def accueil():
    Prospectaccueil = Prospect(1)
    return render_template('accueil.html', title='prospect')

if __name__ == '__main__':
    app.run(debug=True)