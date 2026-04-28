"""Cliente HTTP centralizado para hablar con el backend FastAPI.
Inyecta el JWT automaticamente, lanza ApiException con codigo + mensaje.
Todas las pages usan esta capa, no httpx directamente.
"""

import os
from typing import Any

import httpx

import state

BASE_URL = os.getenv("API_URL", "https://fapp-api.onrender.com/api")


class ApiException(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
        super().__init__(f"[{status}] {message}")


async def _request(method: str, path: str, **kwargs: Any) -> Any:
    headers = kwargs.pop("headers", {})
    token = state.get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    headers["Content-Type"] = "application/json"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(method, f"{BASE_URL}{path}", headers=headers, **kwargs)

    if 200 <= response.status_code < 300:
        return response.json() if response.content else None

    try:
        detail = response.json().get("detail", response.text)
    except Exception:
        detail = response.text or "Unknown error"
    raise ApiException(response.status_code, str(detail))


async def get(path: str, params: dict | None = None) -> Any:
    return await _request("GET", path, params=params)


async def post(path: str, json: dict | None = None) -> Any:
    return await _request("POST", path, json=json)


async def delete(path: str) -> Any:
    return await _request("DELETE", path)


# --- Atajos por dominio (mejor que strings sueltos en cada page) ---

async def login(email: str, password: str) -> dict:
    return await post("/auth/login", {"email": email, "password": password})


async def get_me() -> dict:
    return await get("/auth/me")


async def register(name: str, surname: str, birthdate: str, email: str, password: str) -> dict:
    return await post(
        "/auth/register",
        {
            "name": name,
            "surname": surname,
            "birthdate": birthdate,
            "email": email,
            "password": password,
        },
    )


async def get_dashboard() -> dict:
    return await get("/dashboard")


async def get_categories() -> list[dict]:
    return await get("/categories")


async def get_expenses(category_id: int | None = None) -> list[dict]:
    params = {"category_id": category_id} if category_id else None
    return await get("/expenses", params)


async def create_expense(amount: float, description: str, expense_date: str, category_id: int) -> dict:
    return await post(
        "/expenses",
        {
            "amount": amount,
            "description": description,
            "expense_date": expense_date,
            "category_id": category_id,
        },
    )


async def delete_expense(expense_id: int) -> None:
    await delete(f"/expenses/{expense_id}")


async def get_budgets(month: int, year: int) -> list[dict]:
    return await get("/budgets", {"month": month, "year": year})


async def create_budget(category_id: int, limit_amount: float, month: int, year: int) -> dict:
    return await post(
        "/budgets",
        {
            "category_id": category_id,
            "limit_amount": limit_amount,
            "month": month,
            "year": year,
        },
    )


async def delete_budget(budget_id: int) -> None:
    await delete(f"/budgets/{budget_id}")


async def get_goals() -> list[dict]:
    return await get("/goals")


async def create_goal(name: str, target_amount: float, deadline: str | None) -> dict:
    return await post(
        "/goals",
        {"name": name, "target_amount": target_amount, "deadline": deadline},
    )


async def contribute_goal(goal_id: int, amount: float) -> dict:
    return await post(f"/goals/{goal_id}/contribute", {"amount": amount})


async def delete_goal(goal_id: int) -> None:
    await delete(f"/goals/{goal_id}")


async def get_challenges() -> list[dict]:
    return await get("/challenges")


async def submit_attempt(challenge_id: int, payload: dict) -> dict:
    return await post(f"/challenges/{challenge_id}/attempt", {"payload": payload})
