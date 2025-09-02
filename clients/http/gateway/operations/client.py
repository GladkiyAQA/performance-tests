from typing import TypedDict
from httpx import Response

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client



class OperationDict(TypedDict):
    """
    Описание структуры операции.
    """
    id: str
    type: str
    status: str
    amount: float
    cardId: str
    category: str
    createdAt: str
    accountId: str


class OperationReceiptDict(TypedDict):
    """
    Описание структуры чека по операции.
    """
    url: str
    document: str


class OperationsSummaryDict(TypedDict):
    """
    Описание структуры статистики операций.
    """
    spentAmount: float
    receivedAmount: float
    cashbackAmount: float


class GetOperationResponseDict(TypedDict):
    operation: OperationDict


class GetOperationReceiptResponseDict(TypedDict):
    receipt: OperationReceiptDict


class GetOperationsResponseDict(TypedDict):
    operations: list[OperationDict]


class GetOperationsSummaryResponseDict(TypedDict):
    summary: OperationsSummaryDict


class MakeFeeOperationResponseDict(TypedDict):
    operation: OperationDict


class MakeTopUpOperationResponseDict(TypedDict):
    operation: OperationDict


class MakeCashbackOperationResponseDict(TypedDict):
    operation: OperationDict


class MakeTransferOperationResponseDict(TypedDict):
    operation: OperationDict


class MakePurchaseOperationResponseDict(TypedDict):
    operation: OperationDict


class MakeBillPaymentOperationResponseDict(TypedDict):
    operation: OperationDict


class MakeCashWithdrawalOperationResponseDict(TypedDict):
    operation: OperationDict



class AccountQueryDict(TypedDict):
    accountId: str


class OperationBaseRequestDict(TypedDict):
    status: str
    amount: float
    cardId: str
    accountId: str


class GetOperationsQueryDict(AccountQueryDict):
    ...


class GetOperationsSummaryQueryDict(AccountQueryDict):
    ...


class MakeFeeOperationRequestDict(OperationBaseRequestDict):
    ...


class MakeTopUpOperationRequestDict(OperationBaseRequestDict):
    ...


class MakeCashbackOperationRequestDict(OperationBaseRequestDict):
    ...


class MakeTransferOperationRequestDict(OperationBaseRequestDict):
    ...


class MakePurchaseOperationRequestDict(OperationBaseRequestDict):
    category: str


class MakeBillPaymentOperationRequestDict(OperationBaseRequestDict):
    ...


class MakeCashWithdrawalOperationRequestDict(OperationBaseRequestDict):
    ...



class OperationsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с эндпоинтами /api/v1/operations сервиса http-gateway.
    """


    def get_operation_api(self, operation_id: str) -> Response:
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        return self.get("/api/v1/operations", params=query)

    def get_operations_summary_api(self, query: GetOperationsSummaryQueryDict) -> Response:
        return self.get("/api/v1/operations/operations-summary", params=query)

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)


    def get_operation(self, operation_id: str) -> GetOperationResponseDict:
        response = self.get_operation_api(operation_id)
        return response.json()

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseDict:
        response = self.get_operation_receipt_api(operation_id)
        return response.json()

    def get_operations(self, account_id: str) -> GetOperationsResponseDict:
        query = GetOperationsQueryDict(accountId=account_id)
        response = self.get_operations_api(query)
        return response.json()

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseDict:
        query = GetOperationsSummaryQueryDict(accountId=account_id)
        response = self.get_operations_summary_api(query)
        return response.json()

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseDict:
        request = MakeFeeOperationRequestDict(
            status="COMPLETED",
            amount=55.77,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_fee_operation_api(request)
        return response.json()

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseDict:
        request = MakeTopUpOperationRequestDict(
            status="COMPLETED",
            amount=1500.11,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_top_up_operation_api(request)
        return response.json()

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponseDict:
        request = MakeCashbackOperationRequestDict(
            status="COMPLETED",
            amount=99.99,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_cashback_operation_api(request)
        return response.json()

    def make_transfer_operation(self, card_id: str, account_id: str) -> MakeTransferOperationResponseDict:
        request = MakeTransferOperationRequestDict(
            status="COMPLETED",
            amount=200.00,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_transfer_operation_api(request)
        return response.json()

    def make_purchase_operation(self, card_id: str, account_id: str) -> MakePurchaseOperationResponseDict:
        request = MakePurchaseOperationRequestDict(
            status="COMPLETED",
            amount=321.45,
            cardId=card_id,
            accountId=account_id,
            category="electronics",
        )
        response = self.make_purchase_operation_api(request)
        return response.json()

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> MakeBillPaymentOperationResponseDict:
        request = MakeBillPaymentOperationRequestDict(
            status="COMPLETED",
            amount=870.50,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_bill_payment_operation_api(request)
        return response.json()

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> MakeCashWithdrawalOperationResponseDict:
        request = MakeCashWithdrawalOperationRequestDict(
            status="COMPLETED",
            amount=500.00,
            cardId=card_id,
            accountId=account_id,
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return response.json()



def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Функция создаёт экземпляр OperationsGatewayHTTPClient
    с уже настроенным HTTP-клиентом.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())
