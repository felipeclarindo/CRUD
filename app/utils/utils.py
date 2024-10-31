import requests
from ..modules.exceptions import InvalidResponseError, RequestError
import os

def confirm_exit(response: str) -> bool:
    try:
        if response:
            if response.lower() in ["sim", "s", "não", "nao", "n"]:
                return True
            else:
                raise InvalidResponseError("Responda com Sim/Não")
        else:
            raise InvalidResponseError("Você precisa digitar algo!")
    except InvalidResponseError as e:
        print(f"Error: {e}")
    return False


def confirm_requisition(response: requests.models.Response, method: str):
    try:
        if response.status_code == 200:
            return True
        else:
            raise RequestError(
                f"Erro ao realizar o método {method}, \nverifique as informações informadas e tente novamente. "
            )
    except RequestError as e:
        print(e)
    return False

def check_folder() -> None:
    if not os.path.exists("./app/json") :
        os.mkdir("json")