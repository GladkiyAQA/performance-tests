from httpx import Response

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.documents.schema import (
    GetTariffDocumentResponseSchema,
    GetContractDocumentResponseSchema,
)


class DocumentsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    """

    def get_tariff_document_api(self, account_id: str) -> Response:
        """
        Низкоуровневый метод: получить тариф по счету.
        """
        return self.get(
            f"/api/v1/documents/tariff-document/{account_id}",
            extensions=HTTPClientExtensions(route="/api/v1/documents/tariff-document/{account_id}")
        )

    def get_contract_document_api(self, account_id: str) -> Response:
        """
        Низкоуровневый метод: получить контракт по счету.
        """
        return self.get(
            f"/api/v1/documents/contract-document/{account_id}",
            extensions=HTTPClientExtensions(route="/api/v1/documents/tariff-document/{account_id}")
        )

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        """
        Высокоуровневый метод: получить тарифный документ.
        """
        response = self.get_tariff_document_api(account_id)
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseSchema:
        """
        Высокоуровневый метод: получить контрактный документ.
        """
        response = self.get_contract_document_api(account_id)
        return GetContractDocumentResponseSchema.model_validate_json(response.text)


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Функция создаёт экземпляр DocumentsGatewayHTTPClient с уже настроенным HTTP-клиентом.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())
