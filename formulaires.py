from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    pseudo = StringField('Pseudo :', validators=[DataRequired()])
    mdp = PasswordField('Mot de passe :', validators=[DataRequired()])
    submit = SubmitField('se connecter')