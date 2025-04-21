from flask import Flask, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = 'secreto'  # Requerido por Flask-WTF

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message="Campo obligatorio"),
        Length(min=3, message="Mínimo 3 caracteres")
    ])
    correo = StringField('Correo', validators=[
        DataRequired(message="Campo obligatorio"),
        Email(message="Correo inválido")
    ])
    contraseña = PasswordField('Contraseña', validators=[
        DataRequired(message="Campo obligatorio"),
        Length(min=6, message="Mínimo 6 caracteres")
    ])
    submit = SubmitField('Registrar')

@app.route('/', methods=['GET', 'POST'])
def registrar():
    form = RegistroForm()
    if form.validate_on_submit():
        flash("Usuario registrado correctamente")
        return redirect('/')
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

