# Импортируем фабричные функции для создания API-клиентов
from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.cards.client import build_cards_gateway_grpc_client
from clients.grpc.gateway.users.client import build_users_gateway_grpc_client

# Создаём API-клиенты для работы с сервисами Users, Accounts и Cards
users_gateway_client = build_users_gateway_grpc_client()
cards_gateway_client = build_cards_gateway_grpc_client()
accounts_gateway_client = build_accounts_gateway_grpc_client()

# Шаг 1. Создаём пользователя
create_user_response = users_gateway_client.create_user()
print('Create user response:', create_user_response)

# Шаг 2. Открываем дебетовый счёт для только что созданного пользователя
open_debit_card_account_response = accounts_gateway_client.open_debit_card_account(
    user_id=create_user_response.user.id
)
print('Open debit card account response:', open_debit_card_account_response)

# Шаг 3. Выпускаем физическую карту для указанного счёта и пользователя
issue_physical_card_response = cards_gateway_client.issue_physical_card(
    user_id=create_user_response.user.id,
    account_id=open_debit_card_account_response.account.id
)
print('Issue physical card response:', issue_physical_card_response)

