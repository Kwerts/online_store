import jwt
import os
import time

from fastapi import Depends, Cookie, APIRouter, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from dotenv import load_dotenv

import schemas

from repositories.user import user_repository
from repositories.product import product_repository, \
    categories_repository as product_categories_repository


load_dotenv()

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

jwt_secret_key = os.getenv('JWT_SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
token_availability_in_minutes = 10


async def decode_jwt(jwt_token: str) -> dict:
    try:
        return jwt.decode(jwt=jwt_token, key=jwt_secret_key, algorithms=algorithm)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized')


@router.post('/user/register', status_code=status.HTTP_201_CREATED,
             response_model=schemas.RegisterResponse,
             responses={
                 status.HTTP_201_CREATED: {"description": "User successfully created"},
                 status.HTTP_400_BAD_REQUEST: {"description": "Username already taken"}
             })
async def register_user(user_to_register: schemas.UserRegister):
    existing_user = await user_repository.get_user(username=user_to_register.username)
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Username "{user_to_register.username}" already taken')
    
    hashed_password = pwd_context.hash(user_to_register.password)
    
    user_to_add = schemas.AddUser(**user_to_register.model_dump(), hashed_password=hashed_password)
    
    await user_repository.add_user(user_to_add=user_to_add)
    return schemas.RegisterResponse


@router.post('/user/login', status_code=status.HTTP_200_OK, response_model=schemas.LoginResponse,
             responses={
                 status.HTTP_200_OK: {'description': 'Successful authentication'}, 
                 status.HTTP_400_BAD_REQUEST: {'description': 'Login or password is incorrect'}
             })
async def login_user(response: Response,
                     form: OAuth2PasswordRequestForm = Depends()):
    existing_user = await user_repository.get_user(username=form.username)
    if (not existing_user or 
            not pwd_context.verify(secret=form.password, hash=existing_user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Login or password is incorrect')
        
        
    current_epoch = int(time.time())
    expires = current_epoch + token_availability_in_minutes * 60
    
    data_for_jwt = {
        "user_id": existing_user.id,
        "exp": expires
    }
        
    jwt_token = jwt.encode(payload=data_for_jwt, key=jwt_secret_key, algorithm=algorithm)
    
    response.set_cookie(key='jwt_token', value=jwt_token, 
                        max_age=token_availability_in_minutes * 60, samesite='none')
    return schemas.LoginResponse


@router.post('/user/check/auth', response_model=schemas.CheckAuthenticationResponse,
             responses={
                   status.HTTP_200_OK: {"description": "User is authorized"},
                   status.HTTP_401_UNAUTHORIZED: {"description": "User unauthorized"}
            })
async def check_user_auth(jwt_token: str = Cookie(None)):
    await decode_jwt(jwt_token=jwt_token)
    
    return schemas.CheckAuthenticationResponse
        

@router.get('/products/categories/all')
async def get_all_product_categories() -> list[schemas.CategoryResponse]:
    all_categories = await product_categories_repository.get_all_product_categories()
    return [schemas.CategoryResponse.model_validate(category) for category in all_categories]


@router.post('/products/category', status_code=status.HTTP_201_CREATED,
             response_model=schemas.AddCategoryResponse,
             responses={
                 status.HTTP_201_CREATED: {"description": "Category successfully added"}, 
                 status.HTTP_400_BAD_REQUEST: {"description": "This category already exists"}
            })
async def add_product_category(category_to_add: schemas.AddCategory):
    existing_product_category = (await product_categories_repository.get_product_category
                                 (name=category_to_add.name))
    if existing_product_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='This category already exists')
    
    await product_categories_repository.add_product_category(name=category_to_add.name)

    return schemas.AddCategoryResponse


@router.delete('/products/category/{category_name}', response_model=schemas.DeleteCategoryResponse,
               responses={
                   status.HTTP_200_OK: {"description": "Category successfully deleted"},
                   status.HTTP_404_NOT_FOUND: {"description": "Category to delete not found"}
               })
async def delete_product_category(category_name: str):
    product_category = await product_categories_repository.get_product_category(name=category_name)
    
    if not product_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Category to delete not found')
    
    await product_categories_repository.delete_product_category(product_category=product_category)
    
    return schemas.DeleteCategoryResponse
    


@router.get('/products', response_model=list[schemas.ProductResponse])
async def get_products(category_name: str | None = None):
    products = await product_repository.get_products(category_name=category_name)
    return [schemas.ProductResponse.model_validate(product) for product in products]


@router.get('/products/{product_id}', response_model=schemas.ProductResponse,
            responses={
                 status.HTTP_200_OK: {'description': 'Product found'}, 
                 status.HTTP_404_NOT_FOUND: {'description': 'Product not found'}
            })
async def get_product(product_id: int):
    existing_product = await product_repository.get_product(product_id=product_id)
    
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return schemas.ProductResponse.model_validate(existing_product)


@router.post('/products/my', response_model=list[schemas.ProductResponse])
async def get_my_products(jwt_token: str = Cookie(None)):
    current_user_id = (await decode_jwt(jwt_token=jwt_token))["user_id"]
    user = await user_repository.get_user(user_id=current_user_id)
    user_products = await product_repository.get_user_products(username=user.username)
    
    return [schemas.ProductResponse.model_validate(product) for product in user_products]


@router.post('/products/user/{username}', response_model=list[schemas.ProductResponse],
             responses={
                 status.HTTP_200_OK: {"description": "User found"},
                 status.HTTP_404_NOT_FOUND: {"description": "User not found"}
             })
async def get_user_products(username: str):
    existing_user = await user_repository.get_user(username=username)
    
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    user_products = await product_repository.get_user_products(username=username)
    
    return [schemas.ProductResponse.model_validate(user_product) for user_product in user_products]


@router.post('/products/add', status_code=status.HTTP_201_CREATED,
             response_model=schemas.AddProductResponse)
async def add_product(product_to_add: schemas.AddProduct, jwt_token: str = Cookie(None)):
    current_user_id = (await decode_jwt(jwt_token=jwt_token))["user_id"]
    
    user = await user_repository.get_user(user_id=current_user_id)
    
    product_to_add_to_db = schemas.AddProductToDB(
        **product_to_add.model_dump(),
        added_by_user_username=user.username,
    )
    
    await product_repository.add_product(product_to_add_to_db)
    return schemas.AddProductResponse


@router.delete('/products/delete/{product_id}', response_model=schemas.DeleteProductResponse,
               responses={
                   status.HTTP_200_OK: {"description": "Product successfully deleted."},
                   status.HTTP_404_NOT_FOUND: {"description": "Product to delete not found"}
               })
async def delete_product(product_id: int):
    existing_product = await product_repository.get_product(product_id=product_id)
    
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Product to delete not found')
    
    await product_repository.delete_product(product=existing_product)

    return schemas.DeleteProductResponse
