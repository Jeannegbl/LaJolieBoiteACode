from models import *
from flask import render_template, Flask
from config import Config
from formulaires import RegisterForm


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['get', 'post'])
def index():
    form = RegisterForm()
    return render_template('connexion.html', form=form, title='connexion')


@app.route('/accueil')
def accueil():
    Prospects = Prospectaccueil(1)
    return render_template('accueil.html', title='prospect', prospect=Prospects)


if __name__ == "__main__":
    app.run(debug=True)
