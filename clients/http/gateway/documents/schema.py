from pydantic import BaseModel, ConfigDict


class DocumentSchema(BaseModel):
    """
    Описание структуры документа.
    """
    url: str
    document: str


class GetTariffDocumentResponseSchema(BaseModel):
    """
    Описание ответа при получении тарифного документа.
    """
    tariff: DocumentSchema


class GetContractDocumentResponseSchema(BaseModel):
    """
    Описание ответа при получении контракта.
    """
    contract: DocumentSchema
