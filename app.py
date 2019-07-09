from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# linking the sql database here

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# creating model for the database

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# In the above code we are giving /// for relative path and //// is given for the absolute path
# absolute path is used when we want to specify exact path of object location

# Below function returns a string every time we create a new element
#starting app route decorater over here

@app.route('/', methods=['POST', 'GET'])



def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue in adding the value to the database'
    else:
        # the below statement return all the content in the database based on the date they are created
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# starting new route for delete section of this task master application
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem in deleting you data from the database'

# starting new route for update section of this application
@app.route('/update/<int:id>', methods=['GET', 'POST'])

def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Hey there was an issue occurred while updating your task'

    else:
        return render_template('update.html', task=task)
if __name__ == '__main__':
    app.run(debug=True)