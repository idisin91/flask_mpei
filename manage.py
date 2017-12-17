#!/usr/bi/env python
import os

from app import create_app, db
from app.models import User, Role, News
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, News=News)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('run', Server(host="0.0.0.0:5000"))

if __name__ == '__main__':
    manager.run()
