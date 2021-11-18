import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask_migrate import Migrate

from app import create_app, db, organization_data
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.context_processor
def inject_organization_name():
    return dict(org_name=organization_data.organization_name, org_logo=os.getenv('LOGO_URL'))

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()    

if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0')
