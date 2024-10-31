import json
from ..utils.utils import check_folder

def generate_json_file(response: dict, filename: str) -> str:
    """
    Função para gerar arquivo json de resposta
    """
    check_folder()
    with open(f"./app/json/{filename}", "w", encoding="utf-8") as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)
    
    return f"Arquivo {filename} gerado com sucesso!"