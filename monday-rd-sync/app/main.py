from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# Função para enviar os dados para o RD Station
def send_to_rd_station(name, email, course_interest):
    url = "https://api.rd.services/platform/contacts"
    headers = {
        "Authorization": "Bearer API-KEY",  # Substitua pela sua chave de API
        "Content-Type": "application/json"
    }
    
    data = {
        "name": name,
        "email": email,
        "custom_fields": {
            "course_interest": course_interest
        }
    }

    # Envia os dados para o RD Station
    response = requests.post(url, headers=headers, json=data)

    # Verifique se a resposta foi bem-sucedida
    if response.status_code == 200:
        print(f"Dados enviados para o RD Station com sucesso!")
    else:
        print(f"Erro ao enviar dados: {response.text}")

@app.post("/webhook/monday")
async def webhook(request: Request):
    data = await request.json()

    # Verifica se o desafio foi enviado pelo Monday
    if "challenge" in data:
        return JSONResponse(content={"challenge": data["challenge"]})

    # Extrai os dados recebidos do Monday
    name = data.get("name")
    email = data.get("email")
    course_interest = data.get("course_interest")

    # Verifica se os dados essenciais foram recebidos
    if name and email:
        # Chama a função para enviar para o RD Station
        send_to_rd_station(name, email, course_interest)
    
    return JSONResponse(content={"message": "Dados recebidos com sucesso!"})
