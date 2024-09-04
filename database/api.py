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
    if not data or not isinstance(data, dict):
        return jsonify({"message": "Dados invalidos ou ausentes."}), 400
    crud = Crud()
    response = crud.post(data)
    if response.get("status") == "success":
        return jsonify({"message": response["message"]}), 201
    else:
        return jsonify({"message": response["message"]}), 400


# Criando rota de atualização de um único dado
@app.route("/patch", methods=["PATCH"])
def patch():
    """
    Rota para atualização de um único dado
    """
    datas = request.get_json()
    if not datas:
        return jsonify({"message": "Dados não encontrados."})

    table = datas.get("table")
    id = datas.get("id")
    column = datas.get("column")
    value = datas.get("value")

    if not table or not id or not column or not value:
        return jsonify({"message": response["message"]})

    crud = Crud()
    response = crud.patch(table, id, column, value)
    if response.get("status") == "success":
        return jsonify({"message": response["message"]}), 200
    else:
        return jsonify({"message": response["message"]}), 400


# Criando rota de remoção de dado
@app.route("/delete", methods=["DELETE"])
def delete():
    """
    Rota para deletar dado pelo id
    """
    datas = request.get_json()
    if not datas:
        return jsonify({"message": "Dados não encontrados."})

    table = datas.get("table")
    id = datas.get("id")

    if not table or not id:
        return jsonify({"message": "Parâmetros 'table' e 'id' são obrigatorios."})

    crud = Crud()
    response = crud.delete(table, id)
    if response.get("status") == "success":
        return jsonify({"message": response["message"]}), 200
    else:
        return jsonify({"message": response["message"]}), 400


# Criando rota de pegar dados
@app.route("/get", methods=["GET"])
def get():
    """
    Rota de pegar dados
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


if __name__ == "__main__":
    # Executa a aplicação
    app.run(debug=True, port=5000)
