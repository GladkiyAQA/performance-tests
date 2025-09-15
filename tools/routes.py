from enum import StrEnum


class APIRoutes(StrEnum):
    USERS = "/api/v1/users"
    CARDS = "/api/v1/cards"
    ACCOUNTS = "/api/v1/accounts"
    DOCUMENTS = "/api/v1/documents"
    OPERATIONS = "/api/v1/operations"
