from clients.http.gateway.users.client import build_users_gateway_http_client
from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.documents.client import build_documents_gateway_http_client

# --- инициализация клиентов ---
users_gateway_client = build_users_gateway_http_client()
accounts_gateway_client = build_accounts_gateway_http_client()
documents_gateway_client = build_documents_gateway_http_client()

# --- создаём пользователя ---
create_user_response = users_gateway_client.create_user()
print("Create user response:", create_user_response)

# --- открываем кредитный счёт ---
open_credit_card_account_response = accounts_gateway_client.open_credit_card_account(
    user_id=create_user_response.user.id
)
print("Open credit card account response:", open_credit_card_account_response)

# --- получаем тарифный документ ---
get_tariff_document_response = documents_gateway_client.get_tariff_document(
    account_id=open_credit_card_account_response.account.id
)
print("Get tariff document response:", get_tariff_document_response)

# --- получаем контрактный документ ---
get_contract_document_response = documents_gateway_client.get_contract_document(
    account_id=open_credit_card_account_response.account.id
)
print("Get contract document response:", get_contract_document_response)
