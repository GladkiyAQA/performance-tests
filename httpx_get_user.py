import time

import httpx  # Импортируем библиотеку HTTPX

# Данные для создания пользователя
create_user_payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}

# Выполняем запрос на создание пользователя
create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()

# Выводим полученные данные пользователя
print("Create user response:", create_user_response_data)
print("Status Code:", create_user_response.status_code)

# Выполняем запрос на получение пользователя по ID
get_user_response = httpx.get(
    f"http://localhost:8003/api/v1/users/{create_user_response_data['user']['id']}"
)
get_user_response_data = get_user_response.json()

# Выводим полученные данные
print("Get user response:", get_user_response_data)
print("Status Code:", get_user_response.status_code)
