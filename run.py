import os
from app import create_app


config_name = os.getenv('ENV')
app = create_app('development')

if __name__ == '__main__':
    app.run()
