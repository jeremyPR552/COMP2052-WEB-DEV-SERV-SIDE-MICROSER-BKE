from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import CursoForm, ChangePasswordForm  # Cambiado CursoForm a EventoForm
from app.models import db, Evento, User  # Cambiado Curso a Evento

# Blueprint principal que maneja el dashboard, gestión de eventos y cambio de contraseña
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública (home).
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('La contraseña actual es incorrecta.')  # traducido
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Contraseña actualizada correctamente.')  # traducido
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name == 'Participant':
        eventos = Evento.query.all()
    elif current_user.role.name == 'Admin':
        eventos = Evento.query.all()
    else:
        eventos = Evento.query.filter_by(organizador_id=current_user.id).all()
    return render_template('dashboard.html', eventos=eventos)

@main.route('/eventos', methods=['GET', 'POST'])
@login_required
def eventos():
    """
    Permite crear un nuevo evento. Solo disponible para organizadores o admins.
    """
    form = CursoForm()
    if form.validate_on_submit():
        evento = Evento(
            nombre=form.nombre.data,  # cambio de titulo a nombre
            descripcion=form.descripcion.data,
            organizador_id=current_user.id  # cambio profesor_id a organizador_id
        )
        db.session.add(evento)
        db.session.commit()
        flash("Evento creado correctamente.")  # traducido
        return redirect(url_for('main.dashboard'))

    return render_template('evento_form.html', form=form)  # cambie curso_form.html a evento_form.html

@main.route('/eventos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_evento(id):
    """
    Permite editar un evento existente. Solo si es admin o el organizador dueño.
    """
    evento = Evento.query.get_or_404(id)

    # Validación de permisos
    if current_user.role.name not in ['Admin', 'Organizer'] or (
        evento.organizador_id != current_user.id and current_user.role.name != 'Admin'):
        flash('No tienes permiso para editar este evento.')  # traducido
        return redirect(url_for('main.dashboard'))

    form = CursoForm(obj=evento)

    if form.validate_on_submit():
        evento.nombre = form.nombre.data
        evento.descripcion = form.descripcion.data
        db.session.commit()
        flash("Evento actualizado correctamente.")  # traducido
        return redirect(url_for('main.dashboard'))

    return render_template('evento_form.html', form=form, editar=True)

@main.route('/eventos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_evento(id):
    """
    Elimina un evento si el usuario es admin o su organizador creador.
    """
    evento = Evento.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Organizer'] or (
        evento.organizador_id != current_user.id and current_user.role.name != 'Admin'):
        flash('No tienes permiso para eliminar este evento.')  # traducido
        return redirect(url_for('main.dashboard'))

    db.session.delete(evento)
    db.session.commit()
    flash("Evento eliminado correctamente.")  # traducido
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("No tienes permiso para ver esta página.")  # traducido
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)
