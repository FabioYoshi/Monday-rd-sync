import os
import httpx
from fastapi import FastAPI, HTTPException
from tenacity import retry, wait_exponential_jitter, stop_after_attempt, retry_if_exception_type

# A URL base da API do RD Station (você pode configurar isso em uma variável de ambiente, se necessário)
RD_BASE_URL = os.getenv("RD_BASE_URL", "https://api.rd.services/platform/contacts")
RD_ACCESS_TOKEN = os.getenv("RD_ACCESS_TOKEN", "RD-TOKEN-HERE")  # Substitua pelo seu token real

app = FastAPI()

class RDClient:
    def __init__(self):
        self._headers = {
            "Authorization": f"Bearer {RD_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    @retry(wait=wait_exponential_jitter(initial=1, max=20),
           stop=stop_after_attempt(5),
           retry=retry_if_exception_type(httpx.HTTPError))
    async def upsert_contact(self, contact_payload: dict) -> dict:
        url = f"{RD_BASE_URL}/contacts/upsert"
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(url, json=contact_payload, headers=self._headers)
                resp.raise_for_status()  # Vai levantar erro se o status não for 2xx
                return resp.json()
        except httpx.HTTPStatusError as e:
            print(f"Erro ao enviar para RD Station: {e.response.status_code} - {e.response.text}")
            raise HTTPException(500, detail="Erro ao se comunicar com o RD Station.")

@app.post("/webhook/monday")
async def monday_webhook(request: Request):
    body = await request.json()

    # Verificando os dados recebidos
    name = body.get("name")
    email = body.get("email")
    course_interest = body.get("course_interest")

    if name and email:
        rd_client = RDClient()

        # Montando o payload com os dados recebidos
        contact_payload = {
            "name": name,
            "email": email,
            "custom_fields": {
                "course_interest": course_interest,  # Certifique-se de que este campo existe no RD Station
            }
        }

        # Enviar para o RD Station
        result = await rd_client.upsert_contact(contact_payload)
        
        return {"message": "Dados recebidos e enviados ao RD Station!", "result": result}
    else:
        raise HTTPException(status_code=400, detail="Nome e Email são obrigatórios.")
