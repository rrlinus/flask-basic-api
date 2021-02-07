from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Resource, Api, reqparse, abort, fields, marshal_with
import os
basedir = os.path.abspath('/')
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)
take_post_args = reqparse.RequestParser()
take_post_args.add_argument('task', type=str, help = "Task is required", required=True)
take_post_args.add_argument('summary', type=str, help = "Summary is required", required=True)
take_post_args = reqparse.RequestParser()
take_post_args.add_argument('task', type=str)
take_post_args.add_argument('summary', type=str)
resource_fields = {
    "id":fields.Integer,
    "summary":fields.String,
    "task": fields.String,

}
class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(200))
# db.create_all()
class ToDo(Resource):

    @marshal_with(resource_fields)
    def get(self, todo_id):
        task = TodoModel.query.filter_by(id=todo_id).first()
        if not task:
            return abort(404, "missing")
        return  task

    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = take_post_args.parse_args()
        task = TodoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409, "Already present")
        todo = TodoModel(id = todo_id, task= args['task'], summary= args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201
    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = take_post_args.parse_args()
        task = TodoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(409, "Not present")
        task.task = args.get('task', task.task)
        task.summary = args.get('summary', task.summary)
        db.session.commit()
        return  task
    def delete(self, todo_id):
        task = TodoModel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        db.session.commit()
        return task

class ToDoList(Resource):
    def get(self):
        todo = TodoModel.query.all()
        todos = {}
        for task in todo:
            todos[task.id] = {"task":task.task, "summary":task.summary}
        return todos
api.add_resource(ToDo,'/todos/<int:todo_id>')
api.add_resource(ToDoList,'/todos')
if __name__ == '__main__':
    app.run(debug=True)