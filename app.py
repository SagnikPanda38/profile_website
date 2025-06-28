from flask import Flask, render_template,request,redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
Scss(app, static_dir='static', asset_dir='static', load_paths=['static'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete= db.Column(db.Integer)
    created= db.Column(db.DateTime, default=db.func.current_timestamp())
    def __repr__(self):
        return f'<Task {self.id}>'
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        current_task = request.form['content']
        new_task=MyTask(content=current_task)
        try:
            
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"ERROR: {e}"
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)
@app.route("/delete/<int:id>")
def delete(id: int):
    task_to_delete = MyTask.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f"Error: {e}")
        return f"ERROR: {e}"
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id: int):
    task_to_edit = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        task_to_edit.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"ERROR: {e}"
    else:
        return render_template('update.html', task=task_to_edit)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)             