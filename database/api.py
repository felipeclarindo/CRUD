from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Crud

# Inicializando a aplicação
app = Flask(__name__)
CORS(app)  # Permite que o front-end faça requisições, mesmo em domínios diferentes

# Criando rota principal
@app.route("/")
def index():
    return jsonify(
        {
            "name": "Crud Api",
            "methods": {
                "/posts": "post new data",
                "/get": "get data",
                "/update": "update data",
                "/delete": "delete data",
            },
            "librarys": ["flask", "flask_cors"],
            "developer": "felipeclarindo",
            "github": "https://github.com/felipeclarindo",
        }
    )

# Criando rota de envio de dados
@app.route("/post", methods=["POST"])
def post():
    datas = request.json
    crud = Crud()
    response = crud.post(datas)
    if response["status"] == "success":
        return jsonify({"message": "Dados inseridos no banco de dados com sucesso!"})
    else:
        return jsonify({"message": response["message"]})

# Criando rota de atualização de dados
@app.route("/put", methods=["PUT"])
def put():
    datas = request.json
    id = datas.get('id')
    column = datas.get("column")
    value = datas.get("value")
    crud = Crud()
    response = crud.put(id, column, value)
    if response["status"] == "success":
        return jsonify({"message": "Dados atualizados com sucesso"})
    else:
        return jsonify({"message": response["message"]})

# Criando rota de atualização de um único dado
@app.route("/patch", methods=["PATCH"])
def patch():
    datas = request.json
    table = datas.get("table")
    id = datas.get("id")
    column = datas.get("column")
    value = datas.get("value")
    crud = Crud()
    response = crud.patch(table, id, column, value)
    if response["status"] == "success":
        return jsonify({"message": "Dado atualizado com sucesso"})
    else:
        return jsonify({"message": response["message"]})

# Criando rota de remoção de dado
@app.route("/delete", methods=["DELETE"])
def delete():
    datas = request.json
    table = datas.get("table")
    id = datas.get("id")
    crud = Crud()
    response = crud.delete(table, id)
    if response["status"] == "success":
        return jsonify({"message": "Usuário deletado com sucesso"})
    else:
        return jsonify({"message": response["message"]})

# Criando rota de pegar dados
@app.route("/get", methods=["GET"])
def get():
    data = request.json
    table = data.pop("table")
    crud = Crud()
    response = crud.get(table)
    if response["status"] == "success":
        return jsonify({"message": "Dados recebidos com sucesso"})
    else:
        return jsonify({"message": response["message"]})

# Criando rota de pegar dado com id
@app.route("/get-with-id", methods=["GET"])
def get_with_id():
    datas = request.json
    table = datas.get("table")
    id = datas.get("id")
    crud = Crud()
    response = crud.get_with_id(table, id)
    if response["status"] == "success":
        return jsonify({"message": "Dados recebidos com sucesso"})
    else:
        return jsonify({"message": response["message"]})

if __name__ == "__main__":
    # Executa a aplicação
    app.run(debug=True, port=5000)
