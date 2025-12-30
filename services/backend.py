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

async def update_task_data(
    task_id: int,
    data: dict,
    headers: dict
) -> bool:
    payload = {
        "task_id": task_id,
        **data
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

async def register(username: str, email: str, password: str):
    """
    Registers a new user in the backend.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/users/register",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )
    return response

async def service_delete_task(task_id: int, headers: dict) -> bool:
    """
    Calls the fastapi backend to delete a task by id
    
    :param task_id: id for the task that's going to be deleted
    :type task_id: int
    :return: task succesfully deleted or error during the operation
    :rtype: bool
    """

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{BACKEND_URL}/tasks/{task_id}",
            headers=headers
        )

    return response


