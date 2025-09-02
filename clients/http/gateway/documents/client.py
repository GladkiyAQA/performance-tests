from typing import TypedDict
from httpx import Response

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client



class DocumentDict(TypedDict):
    """
    Описание структуры документа.
    """
    url: str
    document: str


class GetTariffDocumentResponseDict(TypedDict):
    """
    Описание ответа при получении тарифного документа.
    """
    tariff: DocumentDict


class GetContractDocumentResponseDict(TypedDict):
    """
    Описание ответа при получении контракта.
    """
    contract: DocumentDict



class DocumentsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    """

    def get_tariff_document_api(self, account_id: str) -> Response:
        """
        Низкоуровневый метод: получить тариф по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (httpx.Response).
        """
        return self.get(f"/api/v1/documents/tariff-document/{account_id}")

    def get_contract_document_api(self, account_id: str) -> Response:
        """
        Низкоуровневый метод: получить контракт по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (httpx.Response).
        """
        return self.get(f"/api/v1/documents/contract-document/{account_id}")

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseDict:
        """
        Высокоуровневый метод: получить тарифный документ.

        :param account_id: Идентификатор счета.
        :return: JSON-ответ (словарь с ключом 'tariff').
        """
        response = self.get_tariff_document_api(account_id)
        return response.json()

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseDict:
        """
        Высокоуровневый метод: получить контрактный документ.

        :param account_id: Идентификатор счета.
        :return: JSON-ответ (словарь с ключом 'contract').
        """
        response = self.get_contract_document_api(account_id)
        return response.json()



def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Функция создаёт экземпляр DocumentsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())
