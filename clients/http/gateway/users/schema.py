from pydantic import BaseModel, Field, EmailStr, ConfigDict


# Добавили суффикс Schema вместо Dict
class UserSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры пользователя.
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")  # Использовали alise
    first_name: str = Field(alias="firstName")  # Использовали alise
    middle_name: str = Field(alias="middleName")  # Использовали alise
    phone_number: str = Field(alias="phoneNumber")  # Использовали alise


# Добавили суффикс Schema вместо Dict
class GetUserResponseSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры ответа получения пользователя.
    """
    user: UserSchema


# Добавили суффикс Schema вместо Dict
class CreateUserRequestSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Структура данных для создания нового пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    last_name: str = Field(alias="lastName")  # Использовали alise
    first_name: str = Field(alias="firstName")  # Использовали alise
    middle_name: str = Field(alias="middleName")  # Использовали alise
    phone_number: str = Field(alias="phoneNumber")  # Использовали alise


# Добавили суффикс Schema вместо Dict
class CreateUserResponseSchema(BaseModel):  # Наследуем от BaseModel вместо TypedDict
    """
    Описание структуры ответа создания пользователя.
    """
    user: UserSchema
