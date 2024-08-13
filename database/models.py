from dataclasses import dataclass
from config import connect
import json
import sys
import os

@dataclass
class Crud:
    connection = connect()

    # Inserir dados no banco de dados
    def post(self, table:str, dados:dict):
        try:
            for data, value in dados.items():
                command = f"INSERT INTO :table (:data) VALUES (:value))"
                cursor = self.connection.cursor()
                cursor.execute(command, {"table": table, "data": data, "value": value})
                self.connection.commit()
                cursor.close()
                return {"status": "success"}
            else:
                return {"status": "error", "message": "404"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    # Atualizar dados
    def put(self, table:str, datas:dict):
        try:
            for data, value in datas.items():
                command = "UPDATE :table SET :data = :value WHERE ID = :id"
                cursor = self.connection.cursor()
                cursor.execute(command, {"table": table, "data":data, "value":value})
                cursor.close()
                return {"status": "success"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Atualizar selecionando campo
    def patch(self, table:str, idList:list, datas:dict):
        try:
            for cont, data, value in enumerate(datas.items()):
                command = "UPDATE relatos SET :dado = :novo_dado WHERE ID = :id"
                cursor = self.connection.cursor()
                cursor.execute(command, {"table": table, "data":data, "value":value, "id": idList[cont]})
                cursor.close()
                return {"status": "success"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Deletar
    def delete(self, id:int):
        try:
            command = f"DELETE FROM relatos WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, {"id":id})
            self.connection.commit()
            cursor.close()
            return {"status": "success"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Obter todos os dados
    def get(self, table:str):
        try:
            command = "SELECT * FROM :table"
            cursor = self.connection.cursor()
            cursor.execute(command, {"table": table})
            usuarios = cursor.fetchall()
            cursor.close()
            return {"status": "success", "message": json.dumps([dict(usuario) for usuario in usuarios])}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    # Obter dados por ID
    def get_with_id(self, table:str, id:int):
        try:
            command = f"SELECT * FROM :table WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, {"table": table, "id":id})
            usuario = cursor.fetchone()
            cursor.close()
            return {"status": "success", "message": json.dumps([dict(usuario)])}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # Finalizando a conexão quando instancia excluida
    def __del__(self):
        self.connection.close()
