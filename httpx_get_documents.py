import time
import httpx

# Шаг 1: создаём пользователя
create_user_payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}
create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()

# Шаг 2: открываем кредитный счёт
open_credit_card_account_payload = {
    "userId": create_user_response_data["user"]["id"]
}
open_credit_card_account_response = httpx.post(
    "http://localhost:8003/api/v1/accounts/open-credit-card-account",
    json=open_credit_card_account_payload
)
open_credit_card_account_response_data = open_credit_card_account_response.json()

# Шаг 3: получаем тарифный документ
get_tariff_document_response = httpx.get(
    f"http://localhost:8003/api/v1/documents/tariff-document/"
    f"{open_credit_card_account_response_data['account']['id']}"
)
get_tariff_document_response_data = get_tariff_document_response.json()

print("Get tariff document response:", get_tariff_document_response_data)
print("Get tariff document status code:", get_tariff_document_response.status_code)

# Шаг 4: получаем контракт
get_contract_document_response = httpx.get(
    f"http://localhost:8003/api/v1/documents/contract-document/"
    f"{open_credit_card_account_response_data['account']['id']}"
)
get_contract_document_response_data = get_contract_document_response.json()

print("Get contract document response: ", get_contract_document_response_data)
print("Get contract document status code: ", get_contract_document_response.status_code)
