from .models import RDContact
from datetime import datetime
from typing import Dict, Any
from fastapi import HTTPException

def _norm_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except Exception:
        return value  # fallback para valores não válidos

def map_monday_to_rd(monday_payload: dict) -> tuple[RDContact, str, str]:
    """
    Mapeia os dados do Monday para o formato do RD Station.
    """
    # Verifique os dados do payload para garantir que o email e nome estão sendo passados
    email = monday_payload.get("email", None)
    name = monday_payload.get("name", None)

    if not email:
        raise HTTPException(status_code=400, detail="Email é obrigatório.")

    if not name:
        raise HTTPException(status_code=400, detail="Nome é obrigatório.")

    rd_contact = RDContact(
        email=email,
        name=name,
        tags=["monday-sync"],
        custom_fields={"course_interest": monday_payload.get("course_interest", "")}
    )

    return rd_contact, "item_id", "updated_at"
