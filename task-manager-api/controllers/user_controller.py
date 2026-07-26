import re
from database import db
from models.user import User
from models.task import Task
from config.settings import VALID_ROLES, MIN_PASSWORD_LENGTH


class UserController:
    def get_all(self):
        return [{
            'id': u.id, 'name': u.name, 'email': u.email,
            'role': u.role, 'active': u.active,
            'created_at': str(u.created_at), 'task_count': len(u.tasks),
        } for u in User.query.all()], None

    def get_by_id(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None, 'Usuário não encontrado'
        data = user.to_dict()
        data['tasks'] = [t.to_dict() for t in Task.query.filter_by(user_id=user_id).all()]
        return data, None

    def create(self, data):
        error = self._validate_create(data)
        if error:
            return None, error
        user = User()
        user.name = data['name']
        user.email = data['email']
        user.set_password(data['password'])
        user.role = data.get('role', 'user')
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), None

    def update(self, user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None, 'Usuário não encontrado'
        if not data:
            return None, 'Dados inválidos'
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
                return None, 'Email inválido'
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return None, 'Email já cadastrado'
            user.email = data['email']
        if 'password' in data:
            if len(data['password']) < MIN_PASSWORD_LENGTH:
                return None, 'Senha muito curta'
            user.set_password(data['password'])
        if 'role' in data:
            if data['role'] not in VALID_ROLES:
                return None, 'Role inválido'
            user.role = data['role']
        if 'active' in data:
            user.active = data['active']
        db.session.commit()
        return user.to_dict(), None

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return 'Usuário não encontrado'
        for t in Task.query.filter_by(user_id=user_id).all():
            db.session.delete(t)
        db.session.delete(user)
        db.session.commit()
        return None

    def get_user_tasks(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None, 'Usuário não encontrado'
        from controllers.task_controller import _check_overdue
        result = []
        for t in Task.query.filter_by(user_id=user_id).all():
            task_data = {
                'id': t.id, 'title': t.title, 'description': t.description,
                'status': t.status, 'priority': t.priority,
                'created_at': str(t.created_at),
                'due_date': str(t.due_date) if t.due_date else None,
                'overdue': _check_overdue(t),
            }
            result.append(task_data)
        return result, None

    def login(self, data):
        if not data:
            return None, 'Dados inválidos', 400
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return None, 'Email e senha são obrigatórios', 400
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return None, 'Credenciais inválidas', 401
        if not user.active:
            return None, 'Usuário inativo', 403
        return {
            'message': 'Login realizado com sucesso',
            'user': user.to_dict(),
            'token': f'fake-jwt-token-{user.id}',
        }, None, 200

    def _validate_create(self, data):
        if not data:
            return 'Dados inválidos'
        if not data.get('name'):
            return 'Nome é obrigatório'
        if not data.get('email'):
            return 'Email é obrigatório'
        if not data.get('password'):
            return 'Senha é obrigatória'
        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
            return 'Email inválido'
        if len(data['password']) < MIN_PASSWORD_LENGTH:
            return 'Senha deve ter no mínimo 4 caracteres'
        if User.query.filter_by(email=data['email']).first():
            return 'Email já cadastrado'
        if data.get('role', 'user') not in VALID_ROLES:
            return 'Role inválido'
        return None
