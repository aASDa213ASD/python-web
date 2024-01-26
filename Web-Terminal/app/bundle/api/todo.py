from .                  import api_todo
from .models            import db
from ..todo.models      import Todo

from flask              import request, jsonify
from flask_jwt_extended import jwt_required


@api_todo.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todo_dict = [
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status
        }
        for t in todos
    ]
    return jsonify(todo_dict)


@api_todo.route('/todos', methods=['POST'])
@jwt_required()
def new_todo():
    todo_new = request.get_json()
    title = todo_new.get('title')
    description = todo_new.get('description')

    if not (title and description):
        return jsonify('Invalid input data'), 400

    todo = Todo(title=title, description=description, status=False)
    db.session.add(todo)
    db.session.commit()

    return jsonify({"id": todo.id, "title": todo.title}), 201


@api_todo.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify(f'No todo with id {id}'), 404

    item = {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "status": todo.status
    }

    return jsonify(item)


@api_todo.route('/todos/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify({"message": f"Todo with id = {id} not found"}), 404

    new_data = request.get_json()

    if not new_data:
        return jsonify({"message": "No input data provided"}), 400

    if 'title' in new_data:
        todo.title = new_data['title']

    if 'description' in new_data:
        todo.description = new_data['description']

    db.session.commit()

    return jsonify({"message": "Todo was updated"}), 200


@api_todo.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify(f'No todo with id {id}'), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "Todo was deleted"}), 200
