from app import create_app, db
from app.models import Role, User

app = create_app()

with app.app_context():
    # Definir roles en inglés para consistencia
    roles = ['Admin', 'Organizer', 'Participant']
    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            print(f'✅ Role "{role_name}" created.')

    db.session.commit()

    users_data = [
        {
            "username": "Administrator",
            "email": "admin@example.com",
            "password": "admin123",
            "role_name": "Admin"
        },
        {
            "username": "John Organizer",
            "email": "organizer@example.com",
            "password": "organizer123",
            "role_name": "Organizer"
        },
        {
            "username": "Maria Participant",
            "email": "participant@example.com",
            "password": "participant123",
            "role_name": "Participant"
        }
    ]

    for user_info in users_data:
        existing_user = User.query.filter_by(email=user_info['email']).first()
        if not existing_user:
            role = Role.query.filter_by(name=user_info['role_name']).first()
            user = User(
                username=user_info['username'],
                email=user_info['email'],
                role=role
            )
            user.set_password(user_info['password'])  # Método definido en tu modelo
            db.session.add(user)
            print(f'✅ User "{user.username}" created with role "{role.name}".')
        else:
            print(f'ℹ️ User with email {user_info["email"]} already exists.')

    db.session.commit()
    print("✅ All users processed successfully.")
