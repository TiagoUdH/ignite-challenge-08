from flask import Flask
from database import db
from models.snack import Snack

app = Flask(__name__)
app.config["SECRET_KEY"] = "daily-diet-api"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app=app)

if __name__ == "__main__":
  app.run(debug=True)