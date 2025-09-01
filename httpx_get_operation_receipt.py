import time

import httpx

# Шаг 1. Создание пользователя
create_user_payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}

create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()

print("Create user response:", create_user_response_data)
print("Status Code:", create_user_response.status_code)

# Шаг 2. Создание кредитного счёта для пользователя
open_credit_card_account_payload = {
    "userId": f"{create_user_response_data['user']['id']}"
}

open_credit_card_account_response = httpx.post(
    "http://localhost:8003/api/v1/accounts/open-credit-card-account",
    json=open_credit_card_account_payload
)

open_credit_account_response_data = open_credit_card_account_response.json()

print("Create user response:", open_credit_account_response_data)
print("Status Code:", open_credit_card_account_response.status_code)

# Шаг 3. Совершение операции покупки (purchase)
make_purchase_operation_payload = {
    "status": "IN_PROGRESS",
    "amount": 77.99,
    "category": "taxi",
    "cardId": open_credit_account_response_data["account"]["cards"][0]["id"],
    "accountId": open_credit_account_response_data["account"]["id"]
}
make_purchase_operation_response = httpx.post(
    "http://localhost:8003/api/v1/operations/make-top-up-operation",
    json=make_purchase_operation_payload
)
make_purchase_operation_payload_data = make_purchase_operation_response.json()

print("Make top up operation response:", make_purchase_operation_payload_data)
print("Make top up operation status code:", make_purchase_operation_response.status_code)

# Шаг 4. Получение чека по операции
operation_id = make_purchase_operation_payload_data["operation"]["id"]

operation_receipt_response = httpx.get(
    f"http://localhost:8003/api/v1/operations/operation-receipt/{operation_id}"
)

operation_receipt_payload_data = operation_receipt_response.json()

print("Make top up operation response:", operation_receipt_payload_data)
print("Make top up operation status code:", operation_receipt_response.status_code)