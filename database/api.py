from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import Crud

# Inicializando a aplicação
app = Flask(__name__)
# Permite que o front end faça requisições, mesmo em dominios diferentes
CORS(app)

# Instanciando o Crud
crud = Crud()

# Criando rota principal 
@app.route('/')
def index():
    return render_template("form.html")

# Criando rota de envio de dados
@app.route("/post", methods = ['POST'])
def post_relatos(table:str, datas:dict):
    response = crud.post(table, datas)
    if response["status"] == "succes":
        return jsonify({"message":"Dados inseridos no banco de dados com sucesso!"})
    else:
        return jsonify({"message": "404"})

# Criando rota de atualização de dados
@app.route("/put", methods=['PUT'])
def put_relatos(id:int, datas:dict):
    response = crud.put(id, datas)
    if response["status"] == "success":
        return jsonify({"message": "Dados atualizado com sucesso"})
    else:
        return jsonify({"message": "404"})

# Criando rota de atualização de um unico dado
@app.route("/patch")
def patch_relatos(table:str, id:list, datas:dict):
    response = crud.patch(table, id, datas)
    if response["status"] == "succes":
        return jsonify({"message": "Dado atualizados com sucesso"})
    else:
        return jsonify({"message": "404"})

# Criando rota de removação de dado
@app.route("/delete")
def delete_relatos(id:int):
    deleted = crud.delete(id)
    if deleted["status"] == "success":
        return jsonify({"message":"Registro deletado com sucesso!"})
    else:
        return jsonify({"message": "404"})
    
# Criando rota de pegar dados
@app.route("/get", methods=['GET'])
def get_relatos(table:str):
    response = crud.get(table)
    if response["status"] == "success":
        return jsonify({"message": response["message"]})
    else:
        return jsonify({"message": "404"})

# Criando rota de pegar dado com id
@app.route("/get-with-id")
def get_relatos_with_id(table:str, id:int):
    response = crud.get_with_id(table, id)
    if response["status"] == "succes":
        return jsonify({"message": response["message"]})
    else:
        return jsonify({"message": "404"})

if __name__ == "__main__":
    # Executa a aplicação
    app.run(debug=True)
