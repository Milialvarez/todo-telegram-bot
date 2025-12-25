import httpx
from config import API_TOKEN, BACKEND_URL

def auth_headers():
    """
    Returns authorization headers for authenticated backend requests.
    """
    return {
        "Authorization": f"Bearer {API_TOKEN}"
    }

async def fetch_my_tasks():
    """
    Retrieves tasks for the authenticated user.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/tasks/me",
            headers=auth_headers()
        )
    return response

async def create_task(payload: dict):
    """
    Sends a request to create a new task.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/tasks/",
            json=payload,
            headers=auth_headers()
        )
    return response

async def update_task_status(task_id: int, status: str) -> bool:
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

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
