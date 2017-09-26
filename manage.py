"""manage.py."""

import os
import unittest
from flask_script import Manager  # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models import User, Bucketlist, Item

config = os.getenv("ENV")

app = create_app(config_name=config)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# define our command for testing called "test"
# Usage: python manage.py test



if __name__ == '__main__':
    manager.run()
