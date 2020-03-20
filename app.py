from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Nullable means cant be left blank.
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # pass in the id of the input that you want to get the content of.
        task_content = request.form['task_content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()

            return redirect('/')
        except:
            return 'An error occured, please retry.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'An error occured, please retry.'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occured, please retry.'

    else:
        return render_template('update.html', task=task_to_update)


if __name__ == '__main__':
    app.run(debug=True)