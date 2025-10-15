# Monday-rd-sync
This application integrates Monday records with the RD Station lead database.

---

## ⚙️ 6. Instalação e Execução

### 🧾 Pré-requisitos

Antes de iniciar, garanta que você possui instalado:

* **Python 3.9+**
* **pip** (gerenciador de pacotes do Python)
* **Ngrok** (para expor a aplicação local ao Monday.com)
* Conta ativa no **Monday.com** com permissão para criar webhooks
* Conta no **RD Station Marketing** com **token de acesso à API**

---

### 🧩 Passo 1 — Clonar o Repositório

```bash
gh repo clone FabioYoshi/Monday-rd-sync
cd seu-repositorio
```

---

### 📦 Passo 2 — Criar o Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows
```

---

### 🧰 Passo 3 — Instalar as Dependências

```bash
pip install -r requirements.txt
```

---

### 🔑 Passo 4 — Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione:

```ini
RD_ACCESS_TOKEN=seu_token_rdstation_aqui
RD_BASE_URL=https://api.rd.services/platform/contacts
```

> 💡 **Dica:** nunca versione seu `.env` no GitHub. Adicione-o ao `.gitignore`.

---

### 🌐 Passo 5 — Executar o Servidor Localmente

Rode o servidor FastAPI com o **uvicorn**:

```bash
uvicorn main:app --reload
```

Por padrão, o servidor rodará em:
👉 `http://127.0.0.1:8000`

---

### 🚀 Passo 6 — Expor o Servidor com Ngrok

Abra outro terminal e execute:

```bash
ngrok http 8000
```

Copie a URL pública gerada pelo Ngrok (exemplo: `https://abc123.ngrok.io`)
e configure-a como **Webhook URL** no Monday.com.

---

### 🧪 Passo 7 — Testar a Integração

1. Crie ou atualize um item no seu board do **Monday.com**.
2. Verifique os logs no terminal do FastAPI.
3. Confirme no **RD Station** se o lead foi criado ou atualizado corretamente.

---

### 🧼 Passo 8 — (Opcional) Rodar com Docker

Se preferir usar **Docker**, crie um arquivo `Dockerfile` e rode:

```bash
docker build -t monday-rd-integration .
docker run -d -p 8000:8000 --env-file .env monday-rd-integration
```

---

## 🔒 7. Configuração de Credenciais

Alguns valores sensíveis precisam ser **definidos manualmente pelo usuário** antes de rodar a aplicação.
Essas credenciais permitem autenticar as requisições e garantir a segurança da integração entre o **Monday.com**, o **servidor FastAPI** e o **RD Station**.

### 🧩 1. Arquivo `.env`

No arquivo `.env`, complete o valor do token do RD Station e do segredo compartilhado usado pelo webhook do Monday:

```ini
RD_ACCESS_TOKEN="RD-TOKEN-HERE"
WEBHOOK_SHARED_SECRET="PASSWORD-HERE"
```

* **`RD_ACCESS_TOKEN`**: token da sua conta RD Station Marketing.
  Obtenha em: *Configurações → Integrações → API → Gerar Token*.
* **`WEBHOOK_SHARED_SECRET`**: senha que você definirá para validar as requisições recebidas do Monday.com.

---

### 🧠 2. Arquivo `main.py`

No arquivo `main.py`, localize a configuração do cabeçalho de autenticação:

```python
"Authorization": "Bearer API-KEY"
```

Substitua **`API-KEY`** pela sua chave de autenticação do Monday.com (caso esteja utilizando chamadas autenticadas à API).

---

### ⚙️ 3. Arquivo `rd_client.py`

Neste arquivo, verifique a linha que inicializa o token de acesso do RD Station:

```python
RD_ACCESS_TOKEN = os.getenv("RD_ACCESS_TOKEN", "RD-TOKEN-HERE")
```

* O valor **`RD-TOKEN-HERE`** é apenas um fallback (valor padrão).
  Caso o `.env` não seja carregado, este valor será usado — portanto, **garanta que o `.env` contenha o token correto**.

---

### ✅ Verificação Final

* O webhook do Monday deve estar **ativado** e validado.
* O RD Station deve estar **recebendo leads** normalmente.
* Logs do FastAPI devem indicar `Dados recebidos com sucesso!`.

---

# 📡 Integração Monday.com → RD Station

## 🧩 1. Propósito da Aplicação

Esta aplicação foi desenvolvida para **automatizar a integração entre o Monday.com e o RD Station**, permitindo que informações inseridas em uma tabela do Monday sejam automaticamente enviadas para a base de leads do RD Station.

**Problema resolvido:**
Evita a inserção manual de dados, reduz erros e garante que os leads estejam sempre atualizados na plataforma de marketing.

---

## ⚙️ 2. Como a Aplicação Funciona

### 🔗 Webhook no Monday.com

* Cada vez que um item é **criado ou atualizado** no board do Monday.com, o webhook dispara uma requisição `POST` para a aplicação.

### 🚀 Servidor FastAPI

* Recebe os dados do webhook (nome, e-mail, curso de interesse, etc.).
* Se houver um **desafio de verificação** do Monday (para validar o webhook), responde automaticamente com o valor do desafio.
* Valida se os **campos essenciais** (como nome e e-mail) estão presentes.

### 📤 Envio para o RD Station

* Conecta-se à **API do RD Station** utilizando um token de acesso.
* Envia os dados do contato (incluindo campos personalizados) para **criar ou atualizar** o lead.

### 🔁 Retry Automático

* Caso haja falha de comunicação com o RD Station, a aplicação tenta novamente diversas vezes utilizando uma estratégia de **retry exponencial** para garantir confiabilidade.

---

## 🛠️ 3. Tecnologias Utilizadas

| Tecnologia         | Função                                                                   |
| ------------------ | ------------------------------------------------------------------------ |
| **FastAPI**        | Framework Python usado para criar o servidor web que recebe os webhooks. |
| **httpx**          | Biblioteca para envio de requisições HTTP assíncronas ao RD Station.     |
| **tenacity**       | Implementa a lógica de retry em caso de falhas na comunicação.           |
| **Ngrok**          | Expõe o servidor local a uma URL pública acessível pelo Monday.com.      |
| **Monday.com API** | Envia e recebe eventos da tabela do Monday.                              |
| **RD Station API** | Registra e atualiza os leads recebidos.                                  |

---

## 💡 4. Benefícios da Aplicação

* Automatiza a transferência de dados do Monday.com para o RD Station.
* Elimina a necessidade de inserção manual e minimiza erros humanos.
* É escalável — pode processar qualquer quantidade de registros automaticamente.
* Garante **alta confiabilidade** com tentativas automáticas em caso de falhas temporárias.

---

## 🧪 5. Como Demonstrar

1. Crie um novo item no **Monday.com** e observe ele sendo adicionado automaticamente ao **RD Station**.
2. Mostre os **logs** do FastAPI e da função de envio para o RD Station — os dados são processados em **tempo real**.
3. Explique como a aplicação responde ao **desafio de validação** do webhook do Monday.com para autorizar o fluxo.

---

## 📝 Resumo

Esta aplicação integra o **Monday.com** ao **RD Station**, automatizando o envio de leads.
Sempre que um item é criado ou atualizado no Monday, um webhook dispara uma requisição para o servidor desenvolvido em **Python (FastAPI)**.

O servidor valida os campos (nome, e-mail, curso de interesse) e envia os dados para a **API do RD Station**.
Se houver falha de comunicação, o sistema executa **retries automáticos** com backoff exponencial para garantir a entrega.

A aplicação também responde corretamente ao **desafio de verificação do webhook**, permitindo que a integração funcione sem intervenção manual.

---

### 🧰 Tecnologias Principais

* **FastAPI** — servidor web.
* **httpx** — requisições assíncronas.
* **tenacity** — lógica de retries.
* **Ngrok** — exposição pública local.
* **APIs Monday & RD Station** — comunicação e sincronização de leads.

---

### 🚀 Benefícios Principais

✅ Evita inserção manual de dados
✅ Reduz erros humanos
✅ Escalável para qualquer volume de leads
✅ Atualização em tempo real no RD Station
