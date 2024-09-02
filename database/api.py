from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Crud

# Inicializando a aplicação
app = Flask(__name__)
CORS(app)  # Permite que o front-end faça requisições, mesmo em domínios diferentes


# Criando rota principal
@app.route("/")
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
    )


# Criando rota de envio de dados
@app.route("/post", methods=["POST"])
def post():
    """
    Rota para inserção de dados
    """
    data = request.get_json()
    crud = Crud()
    response = crud.post(data)
    if response["status"] == "success":
        return jsonify({"message": response["message"]}), 201
    else:
        return jsonify({"message": response["message"]}), 400


# Criando rota de atualização de dados
@app.route("/put", methods=["PUT"])
def put():
    """
    Rota de atualização de todos os dados
    """
    datas = request.json
    table = datas.get("table")
    id = datas.get("id")
    columns = datas.get("columns")
    values = datas.get("values")
    crud = Crud()
    response = crud.put(table, columns, values, id)
    if response["status"] == "success":
        return jsonify({"message": response["message"]}), 200
    else:
        return jsonify({"message": response["message"]}), 400


# Criando rota de atualização de um único dado
@app.route("/patch", methods=["PATCH"])
def patch():
    """
    Rota para atualização de um único dado
    """
    datas = request.json
    table = datas.get("table")
    id = datas.get("id")
    column = datas.get("column")
    value = datas.get("value")
    crud = Crud()
    response = crud.patch(table, id, column, value)
    if response["status"] == "success":
        return jsonify({"message": response["message"]}), 200
    else:
        return jsonify({"message": response["message"]}), 400


# Criando rota de remoção de dado
@app.route("/delete", methods=["DELETE"])
def delete():
    """
    Rota para deletar dado pelo id
    """
    datas = request.json
    table = datas.get("table")
    id = datas.get("id")
    crud = Crud()
    response = crud.delete(table, id)
    if response["status"] == "success":
        return jsonify({"message": response["message"]}), 200
    else:
        return jsonify({"message": response["message"]}), 400


# Criando rota de pegar dados
@app.route("/get", methods=["GET"])
def get():
    """
    Rota de pegar dados
    """
    data = request.json
    table = data.get("table")
    crud = Crud()
    response = crud.get(table)
    if response["status"] == "success":
        return (
            jsonify({"status": response["status"], "content": response["message"]}),
            200,
        )
    else:
        return jsonify({"message": response["message"]}), 400


# Criando rota de pegar dado com id
@app.route("/get-with-id", methods=["GET"])
def get_with_id():
    """
    Rota de pegar dados pelo id
    """
    data = request.json
    table = data.get("table")
    id = data.get("id")
    crud = Crud()
    response = crud.get_with_id(table, id)
    if response["status"] == "success":
        return (
            jsonify(
                {
                    "message": "Dados recebidos com sucesso",
                    "content": response["message"],
                }
            ),
            200,
        )
    else:
        return jsonify({"message": response["message"]}), 400


if __name__ == "__main__":
    # Executa a aplicação
    app.run(debug=True, port=5000)
