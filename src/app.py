"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




# MÉTODO GET /members
@app.route('/members', methods=['GET'])
def handle_hello():
    try:
        members = jackson_family.get_all_members()
        if not members:  
            return jsonify({"error": "No se encontraron miembros"}), 404
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# MÉTODO GET /obtener miembro por id
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    try:
        member = jackson_family.get_member(id)
        if member:
            return jsonify(member), 200
        return jsonify({"msg": "Miembro no encontrado"}), 404
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

# MÉTODO POST /member
@app.route('/member', methods=['POST'])
def add_member():
    try:
        member = request.json
        if not member:
            return jsonify({"msg": "los datos son incorrectos"}), 404
        new_member = jackson_family.add_member(member)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"Error al agregar a member ": str(e)}), 500


# MÉTODO DELETE /member
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        result = jackson_family.delete_member(id)
        if result["done"]:
            return jsonify(result), 200
        return jsonify({"msg": "Miembro no encontrado"}), 404
    except Exception as e:
        return jsonify({"Erro": str(e)}), 500




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)