from app.repositories.dependencies import select, Product, schemas, async_session


async def get_product(product_id: int) -> Product | None:
    async with async_session() as session:
        product = await session.scalar(select(Product).where(Product.id == product_id))
        return product


async def get_products(category_name: str | None = None) -> list[Product]:
    async with async_session() as session:
        if not category_name:
            products = await session.scalars(select(Product))
        else:
            products = await session.scalars(select(Product).where
                                             (Product.category_name == category_name))
        return reversed(products.all())
    
    
async def get_user_products(username: str) -> list[Product]:
    async with async_session() as session:
        products = await session.scalars(select(Product).where
                                         (Product.added_by_user_username == username))
        return reversed(products.all())
    
    
async def add_product(product: schemas.AddProductToDB):
    async with async_session() as session:
        session.add(Product(**product.model_dump()))
        await session.commit()
        
        
async def delete_product(product: Product):
    async with async_session() as session:
        await session.delete(product)
        await session.commit()