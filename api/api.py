from flask import Flask, request, jsonify
from flask_cors import CORS
from database.models import Crud

# Inicializando a aplicação
app = Flask(__name__)
# Habilitando CORS
CORS(app) 

# Criando rota principal
@app.route("/api", methods=["GET"])
def index():
    """
    Rota principal com algumas informações da api
    """
    return jsonify(
        {
            "name": "Crud Api",
            "methods": {
                "/post": "post new data",
                "/put": "update data",
                "/patch": "update single field",
                "/delete": "delete data",
                "/get": "get data",
                "/get-with-id": "get data by id",
            },
            "libraries": ["flask", "flask_cors"],
            "developer": "felipeclarindo",
            "github": "https://github.com/felipeclarindo",
        }
    ), 200

# Criando rota de envio de dados
@app.route("/api/table/", methods=["POST"])
def post():
    """
    Rota para inserção de dados
    """
    data = request.json
    if not data or not isinstance(data, dict):
        return jsonify({"message": "Dados inválidos ou ausentes."}), 400
    crud = Crud()
    response = crud.post(data)
    if response.get("status") == "success":
        return jsonify({"message": response["message"]}), 201
    else:
        return jsonify({"message": response["message"]}), 400

# Criando rota de atualização de um único dado
@app.route("/api/table/<int:id>", methods=["PATCH"])
def patch(id: int):
    """
    Rota para atualização de um único dado
    """
    datas = request.json
    if not datas:
        return jsonify({"message": "Dados não encontrados."}), 400

    table = datas.get("table")
    column = datas.get("column")
    value = datas.get("value")

    if not table or not column or not value:
        return jsonify({"message": "Parâmetros obrigatórios ausentes."}), 400

    crud = Crud()
    response = crud.patch(table, id, column, value)
    if response.get("status") == "success":
        return jsonify({"message": response["message"]}), 200
    else:
        return jsonify({"message": response["message"]}), 400

# Criando rota de remoção de dado
@app.route("/api/table/<int:id>", methods=["DELETE"])
def delete(id: int):
    """
    Rota para deletar dado pelo id
    """
    table = request.json.get("table")
    
    if not table:
        return jsonify({"message": "Parâmetro 'table' é obrigatório."}), 400

    crud = Crud()
    response = crud.delete(table, id)
    if response.get("status") == "success":
        return jsonify({"message": response["message"]}), 200
    else:
        return jsonify({"message": response["message"]}), 400

# Criando rota de pegar todos os dados
@app.route("/api/table", methods=["GET"])
def get_all():
    """
    Rota para pegar todos os dados
    """
    table = request.args.get("table")
    if not table:
        return jsonify({"message": "Parâmetro 'table' é obrigatório."}), 400
    crud = Crud()
    response = crud.get(table)
    if response.get("status") == "success":
        return (
            jsonify({"status": response.get("status"), "content": response["message"]}),
            200,
        )
    else:
        return jsonify({"message": response["message"]}), 400

# Criando rota de pegar dados com ID específico
@app.route("/api/table/<int:id>", methods=["GET"])
def get_with_id(id: int):
    table = request.args.get("table")
    if not table:
        return jsonify({"message": "Parâmetro 'table' é obrigatório."}), 400
    crud = Crud()
    response = crud.get_with_id(table, id)
    if response.get("status") == "success":
        return (
            jsonify({"status": response.get("status"), "content": response["message"]}),
            200,
        )
    else:
        return jsonify({"message": response["message"]}), 400

if __name__ == "__main__":
    app.run(debug=True, port=3000)
