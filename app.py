from flask import Flask, jsonify, request
from database import db
from models.snack import Snack

app = Flask(__name__)
app.config["SECRET_KEY"] = "daily-diet-api"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app=app)

@app.route('/snacks', methods=["POST"])
def create_snack():
  data = request.json
  
  name = data.get("name")
  description = data.get("description")
  in_diet = data.get("in_diet")
  
  if name and description and in_diet:
    snack = Snack(name=name, description=description, in_diet=in_diet)
    
    db.session.add(snack)
    db.session.commit()
    
    response = {
      "message": "Snack registered successfully",
      "snack_id": snack.id,
      "created_at": snack.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    }
    
    return jsonify(response)
  
  response = {
    "message": "Invalid snack data"
  }
  
  if not name:
    response["name"] = "This field is required"
    
  if not description:
    response["description"] = "This field is required"
    
  if not in_diet:
    response["in_diet"] = "This field is required"
    
  return jsonify(response), 400

if __name__ == "__main__":
  app.run(debug=True)