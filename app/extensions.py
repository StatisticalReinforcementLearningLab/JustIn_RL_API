from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
