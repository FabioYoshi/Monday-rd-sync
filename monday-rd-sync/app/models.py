# models.py
from pydantic import BaseModel
import importlib

class RDContact(BaseModel):
    email: str
    name: str
    tags: list[str] = []
    custom_fields: dict = {}

def get_main_module():
    # Importação dinâmica do main.py para evitar a importação circular
    main_module = importlib.import_module('app.main')
    return main_module.MondayEvent

# Outras classes ou funções podem ser adicionadas aqui
