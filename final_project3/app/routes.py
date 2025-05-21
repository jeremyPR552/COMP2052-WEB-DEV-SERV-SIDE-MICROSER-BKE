from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import EventoForm, ChangePasswordForm
from app.models import db, Evento, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')
            return render_template('cambiar_password.html', form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name == 'Participant':
        eventos = Evento.query.all()
    else:
        eventos = Evento.query.filter_by(organizador_id=current_user.id).all()

    return render_template('dashboard.html', eventos=eventos)

@main.route('/eventos', methods=['GET', 'POST'])
@login_required
def eventos():
    form = EventoForm()
    if form.validate_on_submit():
        evento = Evento(
            nombre=form.nombre.data,
            ubicacion=form.ubicacion.data,
            fecha=form.fecha.data,
            descripcion=form.descripcion.data,
            organizador_id=current_user.id
        )
        db.session.add(evento)
        db.session.commit()
        flash("Event created successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('evento_form.html', form=form)

@main.route('/eventos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_evento(id):
    evento = Evento.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Organizer'] or (
        evento.organizador_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to edit this event.')
        return redirect(url_for('main.dashboard'))

    form = EventoForm(obj=evento)

    if form.validate_on_submit():
        evento.nombre = form.nombre.data
        evento.ubicacion = form.ubicacion.data
        evento.fecha = form.fecha.data
        evento.descripcion = form.descripcion.data
        db.session.commit()
        flash("Event updated successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('evento_form.html', form=form, editar=True)

@main.route('/eventos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_evento(id):
    evento = Evento.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Organizer'] or (
        evento.organizador_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to delete this event.')
        return redirect(url_for('main.dashboard'))

    db.session.delete(evento)
    db.session.commit()
    flash("Event deleted successfully.")
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))

    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)
