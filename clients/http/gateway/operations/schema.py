from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class OperationType(StrEnum):
    FEE = "FEE"
    TOP_UP = "TOP_UP"
    PURCHASE = "PURCHASE"
    CASHBACK = "CASHBACK"
    TRANSFER = "TRANSFER"
    BILL_PAYMENT = "BILL_PAYMENT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"


class OperationStatus(StrEnum):
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    UNSPECIFIED = "UNSPECIFIED"


class OperationSchema(BaseModel):
    """
    Описание структуры операции.
    """
    id: str
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: str = Field(alias="cardId")
    category: str
    created_at: datetime = Field(alias="createdAt")
    account_id: str = Field(alias="accountId")


class OperationReceiptSchema(BaseModel):
    """
    Описание структуры чека по операции.
    """
    url: str
    document: str


class OperationsSummarySchema(BaseModel):
    """
    Описание структуры статистики операций.
    """
    spent_amount: float = Field(alias="spentAmount")
    received_amount: float = Field(alias="receivedAmount")
    cashback_amount: float = Field(alias="cashbackAmount")


# --- Ответы API --- #

class GetOperationResponseSchema(BaseModel):
    operation: OperationSchema


class GetOperationReceiptResponseSchema(BaseModel):
    receipt: OperationReceiptSchema


class GetOperationsResponseSchema(BaseModel):
    operations: list[OperationSchema]


class GetOperationsSummaryResponseSchema(BaseModel):
    summary: OperationsSummarySchema


class MakeFeeOperationResponseSchema(BaseModel):
    operation: OperationSchema


class MakeTopUpOperationResponseSchema(BaseModel):
    operation: OperationSchema


class MakeCashbackOperationResponseSchema(BaseModel):
    operation: OperationSchema


class MakeTransferOperationResponseSchema(BaseModel):
    operation: OperationSchema


class MakePurchaseOperationResponseSchema(BaseModel):
    operation: OperationSchema


class MakeBillPaymentOperationResponseSchema(BaseModel):
    operation: OperationSchema


class MakeCashWithdrawalOperationResponseSchema(BaseModel):
    operation: OperationSchema


# --- Запросы API --- #

class GetOperationsQuerySchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class GetOperationsSummaryQuerySchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class OperationBaseRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status: OperationStatus
    amount: float
    card_id: str = Field(alias="cardId")
    account_id: str = Field(alias="accountId")


class MakeFeeOperationRequestSchema(OperationBaseRequestSchema):
    ...


class MakeTopUpOperationRequestSchema(OperationBaseRequestSchema):
    ...


class MakeCashbackOperationRequestSchema(OperationBaseRequestSchema):
    ...


class MakeTransferOperationRequestSchema(OperationBaseRequestSchema):
    ...


class MakePurchaseOperationRequestSchema(OperationBaseRequestSchema):
    category: str


class MakeBillPaymentOperationRequestSchema(OperationBaseRequestSchema):
    ...


class MakeCashWithdrawalOperationRequestSchema(OperationBaseRequestSchema):
    ...
