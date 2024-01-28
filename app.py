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
  in_diet = 'in_diet' in data
  
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

@app.route('/snacks/<int:snack_id>', methods=["PUT"])
def update_snack(snack_id):
  snack = db.session.get(Snack, snack_id)
  
  if not snack:
    return jsonify({"message": "Snack not found"}), 404
  
  data = request.json
  
  if 'name' in data:
    snack.name = data["name"]
    
  if 'description' in data:
    snack.description = data["description"]
    
  if 'in_diet' in data:
    snack.in_diet = data["in_diet"]
    
  db.session.commit()
  
  return jsonify({"message": "Snack updated successfully"})
    

if __name__ == "__main__":
  app.run(debug=True)