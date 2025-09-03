import grpc  # Импорт основной библиотеки для работы с gRPC

# Импорты gRPC stub-классов и сообщений запроса/ответа из автогенерированных контрактов
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.accounts.rpc_open_credit_card_account_pb2 import (
    OpenCreditCardAccountRequest,
    OpenCreditCardAccountResponse
)

from contracts.services.gateway.cards.cards_gateway_service_pb2_grpc import CardsGatewayServiceStub
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import (
    IssuePhysicalCardRequest,
    IssuePhysicalCardResponse
)

from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub

# Импорт генератора случайных персональных данных
from tools.fakers import fake

# Устанавливаем соединение с gRPC-шлюзом, который слушает на порту 9003
channel = grpc.insecure_channel("localhost:9003")

# Создаём stub'ы (клиентские обёртки) для взаимодействия с соответствующими gRPC-сервисами
users_gateway_service = UsersGatewayServiceStub(channel)
accounts_gateway_service = AccountsGatewayServiceStub(channel)
cards_gateway_service = CardsGatewayServiceStub(channel)

# 1. Создание нового пользователя
create_user_request = CreateUserRequest(
    email=fake.email(),
    last_name=fake.last_name(),
    first_name=fake.first_name(),
    middle_name=fake.middle_name(),
    phone_number=fake.phone_number()
)
create_user_response: CreateUserResponse = users_gateway_service.CreateUser(create_user_request)

# Логируем ответ
print('Create user response:', create_user_response)

# 2. Открытие кредитного счёта на имя созданного пользователя
open_credit_card_account_request = OpenCreditCardAccountRequest(
    user_id=create_user_response.user.id
)
open_credit_card_account_response: OpenCreditCardAccountResponse = (
    accounts_gateway_service.OpenCreditCardAccount(open_credit_card_account_request)
)

# Логируем ответ
print('Open credit card account response:', open_credit_card_account_response)

# 3. Выпуск физической карты к открытому счёту
issue_physical_card_request = IssuePhysicalCardRequest(
    user_id=create_user_response.user.id,
    account_id=open_credit_card_account_response.account.id
)
issue_physical_card_response: IssuePhysicalCardResponse = (
    cards_gateway_service.IssuePhysicalCard(issue_physical_card_request)
)

# Логируем ответ
print('Issue physical card response:', issue_physical_card_response)
