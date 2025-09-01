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
create_user_response = httpx.post(
    "http://localhost:8003/api/v1/users",
    json=create_user_payload
)
create_user_response_data = create_user_response.json()

# Выводим полученные данные пользователя
print("Create user response:", create_user_response_data)
print("Status Code:", create_user_response.status_code)

# Данные для открытия депозитного счета
open_deposit_account_payload = {
    "userId": f"{create_user_response_data['user']['id']}"
}

# Выполняем запрос на открытие депозитного счета

open_deposit_account_response = httpx.post(
    "http://localhost:8003/api/v1/accounts/open-deposit-account",
    json=open_deposit_account_payload
)

open_deposit_account_response_data = open_deposit_account_response.json()

# Выводим полученные данные об открытии счета
print("Create user response:", open_deposit_account_response_data)
print("Status Code:", open_deposit_account_response.status_code)


