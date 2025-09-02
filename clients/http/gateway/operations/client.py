from typing import TypedDict
from httpx import Response

from clients.http.client import HTTPClient


# ---------- Base TypedDicts ----------

class AccountQueryDict(TypedDict):
    """
    Базовый query-параметр для запросов, где требуется accountId.
    """
    accountId: str


class OperationBaseRequestDict(TypedDict):
    """
    Базовая структура тела POST-запроса для операций.
    """
    status: str
    amount: float
    cardId: str
    accountId: str


# ---------- Specialized Query TypedDicts ----------

class GetOperationsQueryDict(AccountQueryDict):
    """
    Query для GET /api/v1/operations.
    """
    ...


class GetOperationsSummaryQueryDict(AccountQueryDict):
    """
    Query для GET /api/v1/operations/operations-summary.
    """
    ...


# ---------- Specialized Request TypedDicts ----------

class MakeFeeOperationRequestDict(OperationBaseRequestDict):
    """
    Тело запроса для POST /api/v1/operations/make-fee-operation.
    """
    ...


class MakeTopUpOperationRequestDict(OperationBaseRequestDict):
    """
    Тело запроса для POST /api/v1/operations/make-top-up-operation.
    """
    ...


class MakeCashbackOperationRequestDict(OperationBaseRequestDict):
    """
    Тело запроса для POST /api/v1/operations/make-cashback-operation.
    """
    ...


class MakeTransferOperationRequestDict(OperationBaseRequestDict):
    """
    Тело запроса для POST /api/v1/operations/make-transfer-operation.
    """
    ...


class MakePurchaseOperationRequestDict(OperationBaseRequestDict):
    """
    Тело запроса для POST /api/v1/operations/make-purchase-operation.
    """
    category: str


class MakeBillPaymentOperationRequestDict(OperationBaseRequestDict):
    """
    Тело запроса для POST /api/v1/operations/make-bill-payment-operation.
    """
    ...


class MakeCashWithdrawalOperationRequestDict(OperationBaseRequestDict):
    """
    Тело запроса для POST /api/v1/operations/make-cash-withdrawal-operation.
    """
    ...


# ---------- Client ----------

class OperationsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с эндпоинтами /api/v1/operations сервиса http-gateway.
    """

    def get_operation_api(self, operation_id: str) -> Response:
        """
        Получить информацию об операции по её идентификатору.

        :param operation_id: UUID операции.
        :return: Ответ от сервера (httpx.Response).
        """
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """
        Получить чек по операции.

        :param operation_id: UUID операции.
        :return: Ответ от сервера (httpx.Response).
        """
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        """
        Получить список операций для счёта.

        :param query: Словарь с параметром accountId.
        :return: Ответ от сервера (httpx.Response).
        """
        return self.get("/api/v1/operations", params=query)

    def get_operations_summary_api(self, query: GetOperationsSummaryQueryDict) -> Response:
        """
        Получить сводную статистику операций для счёта.

        :param query: Словарь с параметром accountId.
        :return: Ответ от сервера (httpx.Response).
        """
        return self.get("/api/v1/operations/operations-summary", params=query)

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """
        Создать операцию комиссии.

        :param request: Данные операции (status, amount, cardId, accountId).
        :return: Ответ от сервера (httpx.Response).
        """
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """
        Создать операцию пополнения.

        :param request: Данные операции (status, amount, cardId, accountId).
        :return: Ответ от сервера (httpx.Response).
        """
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """
        Создать операцию кэшбэка.

        :param request: Данные операции (status, amount, cardId, accountId).
        :return: Ответ от сервера (httpx.Response).
        """
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """
        Создать операцию перевода.

        :param request: Данные операции (status, amount, cardId, accountId).
        :return: Ответ от сервера (httpx.Response).
        """
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """
        Создать операцию покупки.

        :param request: Данные операции (status, amount, cardId, accountId, category).
        :return: Ответ от сервера (httpx.Response).
        """
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        """
        Создать операцию оплаты по счёту.

        :param request: Данные операции (status, amount, cardId, accountId).
        :return: Ответ от сервера (httpx.Response).
        """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        """
        Создать операцию снятия наличных.

        :param request: Данные операции (status, amount, cardId, accountId).
        :return: Ответ от сервера (httpx.Response).
        """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)
