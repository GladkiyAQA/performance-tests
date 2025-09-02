from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    """
    Модель данных пользователя.

    Пример структуры:
    {
      "id": "string",
      "email": "user@example.com",
      "lastName": "string",
      "firstName": "string",
      "middleName": "string",
      "phoneNumber": "string"
    }
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")


class CreateUserRequestSchema(BaseModel):
    """
    Тело запроса на создание пользователя.

    Пример структуры:
    {
      "email": "user@example.com",
      "lastName": "string",
      "firstName": "string",
      "middleName": "string",
      "phoneNumber": "string"
    }
    """
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")


class CreateUserResponseSchema(BaseModel):
    """
    Ответ сервиса при успешном создании пользователя.

    Пример структуры:
    {
      "user": {
        "id": "string",
        "email": "user@example.com",
        "lastName": "string",
        "firstName": "string",
        "middleName": "string",
        "phoneNumber": "string"
      }
    }
    """
    user: UserSchema
