import httpx
from config import BACKEND_URL

async def fetch_my_tasks(headers: dict):
    """
    Retrieves tasks for the authenticated user.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/tasks/me",
            headers=headers
        )
    return response

async def create_task(payload: dict, headers: dict):
    """
    Sends a request to create a new task.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/tasks/",
            json=payload,
            headers=headers
        )
    return response

async def update_task_status(task_id: int, status: str, headers: dict) -> bool:
    """
    Send the proper dto expected in my fastapi backend
    """
    payload = {
        "task_id": task_id,
        "status": status
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BACKEND_URL}/tasks/",
            json=payload,
            headers=headers
        )

    return response.status_code == 200

async def login(email: str, password: str) -> str | None:
    """
    Performs login against the backend and returns a JWT access token.
    Returns None if authentication fails.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/auth/login",
            data={
                "username": email,
                "password": password
            }
        )

    if response.status_code != 200:
        return None

    return response.json().get("access_token")