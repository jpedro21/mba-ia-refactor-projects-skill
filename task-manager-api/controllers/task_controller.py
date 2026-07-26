from datetime import datetime, timezone
from database import db
from models.task import Task
from models.user import User
from models.category import Category
from config.settings import VALID_STATUSES, MIN_TITLE_LENGTH, MAX_TITLE_LENGTH, DEFAULT_PRIORITY


def _check_overdue(task):
    if task.due_date and task.due_date < datetime.now(timezone.utc).replace(tzinfo=None):
        if task.status not in ('done', 'cancelled'):
            return True
    return False


def _task_to_dict_enriched(task):
    data = task.to_dict()
    data['overdue'] = _check_overdue(task)
    if task.user_id:
        user = User.query.get(task.user_id)
        data['user_name'] = user.name if user else None
    else:
        data['user_name'] = None
    if task.category_id:
        cat = Category.query.get(task.category_id)
        data['category_name'] = cat.name if cat else None
    else:
        data['category_name'] = None
    return data


class TaskController:
    def get_all(self):
        tasks = Task.query.all()
        return [_task_to_dict_enriched(t) for t in tasks], None

    def get_by_id(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return None, 'Task não encontrada'
        data = task.to_dict()
        data['overdue'] = _check_overdue(task)
        return data, None

    def create(self, data):
        error = self._validate_create(data)
        if error:
            return None, error
        task = Task()
        task.title = data['title']
        task.description = data.get('description', '')
        task.status = data.get('status', 'pending')
        task.priority = data.get('priority', DEFAULT_PRIORITY)
        task.user_id = data.get('user_id')
        task.category_id = data.get('category_id')
        if data.get('due_date'):
            try:
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            except ValueError:
                return None, 'Formato de data inválido. Use YYYY-MM-DD'
        if data.get('tags'):
            task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
        db.session.add(task)
        db.session.commit()
        return task.to_dict(), None

    def update(self, task_id, data):
        task = Task.query.get(task_id)
        if not task:
            return None, 'Task não encontrada'
        if not data:
            return None, 'Dados inválidos'
        if 'title' in data:
            if len(data['title']) < MIN_TITLE_LENGTH or len(data['title']) > MAX_TITLE_LENGTH:
                return None, 'Título deve ter entre 3 e 200 caracteres'
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            if data['status'] not in VALID_STATUSES:
                return None, 'Status inválido'
            task.status = data['status']
        if 'priority' in data:
            if data['priority'] < 1 or data['priority'] > 5:
                return None, 'Prioridade deve ser entre 1 e 5'
            task.priority = data['priority']
        if 'user_id' in data:
            if data['user_id'] and not User.query.get(data['user_id']):
                return None, 'Usuário não encontrado'
            task.user_id = data['user_id']
        if 'category_id' in data:
            if data['category_id'] and not Category.query.get(data['category_id']):
                return None, 'Categoria não encontrada'
            task.category_id = data['category_id']
        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                except ValueError:
                    return None, 'Formato de data inválido'
            else:
                task.due_date = None
        if 'tags' in data:
            task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
        task.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.session.commit()
        return task.to_dict(), None

    def delete(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return 'Task não encontrada'
        db.session.delete(task)
        db.session.commit()
        return None

    def search(self, query, status, priority, user_id):
        tasks = Task.query
        if query:
            tasks = tasks.filter(db.or_(Task.title.like(f'%{query}%'), Task.description.like(f'%{query}%')))
        if status:
            tasks = tasks.filter(Task.status == status)
        if priority:
            tasks = tasks.filter(Task.priority == int(priority))
        if user_id:
            tasks = tasks.filter(Task.user_id == int(user_id))
        return [t.to_dict() for t in tasks.all()], None

    def stats(self):
        total = Task.query.count()
        done = Task.query.filter_by(status='done').count()
        all_tasks = Task.query.all()
        overdue_count = sum(1 for t in all_tasks if _check_overdue(t))
        return {
            'total': total,
            'pending': Task.query.filter_by(status='pending').count(),
            'in_progress': Task.query.filter_by(status='in_progress').count(),
            'done': done,
            'cancelled': Task.query.filter_by(status='cancelled').count(),
            'overdue': overdue_count,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
        }, None

    def _validate_create(self, data):
        if not data:
            return 'Dados inválidos'
        title = data.get('title')
        if not title:
            return 'Título é obrigatório'
        if len(title) < MIN_TITLE_LENGTH or len(title) > MAX_TITLE_LENGTH:
            return 'Título deve ter entre 3 e 200 caracteres'
        if data.get('status', 'pending') not in VALID_STATUSES:
            return 'Status inválido'
        if data.get('priority', DEFAULT_PRIORITY) < 1 or data.get('priority', DEFAULT_PRIORITY) > 5:
            return 'Prioridade deve ser entre 1 e 5'
        if data.get('user_id') and not User.query.get(data['user_id']):
            return 'Usuário não encontrado'
        if data.get('category_id') and not Category.query.get(data['category_id']):
            return 'Categoria não encontrada'
        return None
