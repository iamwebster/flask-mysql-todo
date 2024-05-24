from app import app 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv 
import os 


load_dotenv()


app.config['SQLALCHEMY_DATABASE_URI'] = f"""mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@localhost/{os.getenv('MYSQL_DATABASE')}"""

db = SQLAlchemy(app)
