from .           import todo
from ..render    import render


from flask       import redirect, request, url_for
from flask_login import current_user, login_required
from .models     import Todo, db
from .forms      import TODOForm


@todo.route("/todo", methods=["GET", "POST"])
@login_required
def todo_list():
    form = TODOForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        due_date = form.due_date.data
        todo = Todo(user_id=current_user.id, title=title, description=description, due_date=due_date, status=False)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todo.todo_list"))
    
    if current_user.is_authenticated:
        return render("routes/todo.html", route=request.path, form=form, todo_list=reversed(db.session.query(Todo).filter_by(user_id=current_user.id).all()))

    return redirect(url_for("accounts.login"))


@todo.route("/todo_status/<int:id>")
def todo_status(id):
    todo = Todo.query.get(id)
    todo.status = not todo.status
    db.session.commit()
    return redirect(url_for("todo.todo_list"))


@todo.route("/todo_remove/<int:id>")
def todo_remove(id):
    db.session.delete(Todo.query.get(id))
    db.session.commit()
    return redirect(url_for("todo.todo_list"))