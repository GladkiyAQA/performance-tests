import time

import httpx

# Инициализируем клиент с авторизацией
client = httpx.Client(
    base_url="http://localhost:8003",
    timeout=100,
    headers={"Authorization": "Bearer ..."}
)

payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}

# Выполняем запрос с авторизацией
response = client.post("/api/v1/users", json=payload)
print(response.text)

