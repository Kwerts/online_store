from pydantic import BaseModel, EmailStr, ConfigDict
from fastapi import Form

from typing import Annotated


class BaseResponse(BaseModel):
    message: str


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserRegister(UserBase):
    password: str
    
    
class AddUser(UserBase):
    hashed_password: str
    
    
class RegisterResponse(BaseResponse):
    message: str = 'Successfull registration'
    
    
class LoginResponse(BaseResponse):
    message: str = 'Successfull authentication'
    
    
class CheckAuthenticationResponse(BaseResponse):
    message: str = 'User is authorized'
    
    
class CategoryBase(BaseModel):
    name: str
    
    
class CategoryResponse(CategoryBase):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class AddCategory(CategoryBase):
    pass


class AddCategoryToDB(CategoryBase):
    pass


class AddCategoryResponse(BaseResponse):
    message: str = 'Category successfull added'
    
    
class DeleteCategoryResponse(BaseResponse):
    message: str = 'Category successfull deleted'
    
    
class ProductBase(BaseModel):
    name: str
    description: str
    price: Annotated[int, Form(description='Price in dollars', gt=0, title='Price in dollars')]
    
    
class AddProduct(ProductBase):
    category_name: str
    
    model_config = ConfigDict(from_attributes=True)


class AddProductToDB(ProductBase):
    category_name: str
    added_by_user_username: str
    
    
class ProductResponse(ProductBase):
    id: int
    category_name: str
    added_by_user_username: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class ProductInDB(ProductBase):
    id: int
    category_id: int
    
    model_config = ConfigDict(from_attributes=True)


class AddProductResponse(BaseResponse):
    message: str = 'Product successfull added'
    
    
class DeleteProductResponse(BaseResponse):
    message: str = 'Product successfull deleted'