import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Conexión a la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para el auto
class Auto(db.Model):
    __tablename__ = 'autos'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    sucursal = db.Column(db.String(100), nullable=False)
    aspirante = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "marca": self.marca,
            "sucursal": self.sucursal,
            "aspirante": self.aspirante
        }

@app.route('/')
def root():
    return "Home"

# Obtener todos los autos
@app.route('/autos', methods=['GET'])
def get_autos():
    autos = Auto.query.all()
    autos_dict = [auto.to_dict() for auto in autos]
    return jsonify(autos_dict), 200

# Buscar un auto por su ID
@app.route("/autos/<int:id_auto>", methods=['GET'])
def get_auto(id_auto):
    auto = Auto.query.get_or_404(id_auto)
    return jsonify(auto.to_dict()), 200

# Crear un auto nuevo
@app.route('/autos', methods=['POST'])
def create_auto():
    data = request.get_json()
    nuevo_auto = Auto(
        marca=data['marca'],
        sucursal=data['sucursal'],
        aspirante=data['aspirante']
    )
    db.session.add(nuevo_auto)
    db.session.commit()
    data['status'] = "Se ha creado el carro"
    return jsonify(nuevo_auto.to_dict()), 201

# Actualizar datos de un auto
@app.route('/autos/<int:id_auto>', methods=['PUT'])
def update_auto(id_auto):
    auto = Auto.query.get_or_404(id_auto)
    data = request.get_json()
    auto.marca = data.get('marca', auto.marca)
    auto.sucursal = data.get('sucursal', auto.sucursal)
    auto.aspirante = data.get('aspirante', auto.aspirante)
    db.session.commit()
    return jsonify(auto.to_dict()), 200

# Eliminar un auto
@app.route('/autos/<int:id_auto>', methods=['DELETE'])
def delete_auto(id_auto):
    auto = Auto.query.get_or_404(id_auto)
    db.session.delete(auto)
    db.session.commit()
    return jsonify({"mensaje": f"Auto con ID {id_auto} eliminado"}), 200

if __name__ == '__main__':
    app.run(debug=True)