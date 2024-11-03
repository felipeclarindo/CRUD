from flask import Flask, request, jsonify
from flask_cors import CORS
from database.models import Crud

# Inicializando a aplicação
app = Flask(__name__)
CORS(app)  # Habilitando CORS

# Rota principal com informações da API
@app.route("/api", methods=["GET"])
def index():
    return jsonify({
        "name": "Crud Api",
        "endpoints": {
            "/api/table": {
                "methods": {
                    "POST": "post new data",
                    "PATCH": "update single field",
                    "DELETE": "delete data",
                    "GET": "get all data or data by id",
                }
            }
        },
        "libraries": ["flask", "flask_cors"],
        "developer": "felipeclarindo",
        "github": "https://github.com/felipeclarindo"
    }), 200

# Rota para inserção de dados
@app.route("/api/table", methods=["POST"])
def post():
    data = request.json
    if not data or not isinstance(data, dict):
        return jsonify({"message": "Dados inválidos ou ausentes."}), 400
    
    crud = Crud()
    response = crud.post(data)
    return jsonify(response), (201 if response["status"] == "success" else 400)

# Rota para pegar todos os dados
@app.route("/api/table", methods=["GET"])
def get_all():
    table = request.json.get("table")
    if not table:
        return jsonify({"message": "Parâmetro 'table' é obrigatório."}), 400

    crud = Crud()
    response = crud.get(table)
    return jsonify(response), (200 if response["status"] == "success" else 400)

# Rota para pegar dados por ID específico
@app.route("/api/table/<int:id>", methods=["GET"])
def get_with_id(id: int):
    table = request.json.get("table")
    if not table:
        return jsonify({"message": "Parâmetro 'table' é obrigatório."}), 400

    crud = Crud()
    response = crud.get_with_id(table, id)
    return jsonify(response), (200 if response["status"] == "success" else 400)

# Rota para atualização de um único campo de um dado
@app.route("/api/table/<int:id>", methods=["PATCH"])
def patch(id: int):
    data = request.json
    if not data:
        return jsonify({"message": "Dados não encontrados."}), 400

    table = data.get("table")
    column = data.get("column")
    value = data.get("value")

    if not table or not column or not value:
        return jsonify({"message": "Parâmetros obrigatórios ausentes."}), 400

    crud = Crud()
    response = crud.patch(table, id, column, value)
    return jsonify(response), (200 if response["status"] == "success" else 400)

# Rota para deletar dado pelo ID
@app.route("/api/table/<int:id>", methods=["DELETE"])
def delete(id: int):
    table = request.json.get("table") if request.json else None
    if not table:
        return jsonify({"message": "Parâmetro 'table' é obrigatório."}), 400

    crud = Crud()
    response = crud.delete(table, id)
    return jsonify(response), (200 if response["status"] == "success" else 400)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
