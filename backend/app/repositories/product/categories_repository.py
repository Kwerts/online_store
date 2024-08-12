from repositories.dependencies import select, ProductCategory, async_session


async def get_product_category(name: str) -> ProductCategory:
    async with async_session() as session:
        category = await session.scalar(select(ProductCategory).where
                                        (ProductCategory.name == name))
        return category
    
    
async def get_all_product_categories() -> list[ProductCategory]:
    async with async_session() as session:
        categories = await session.scalars(select(ProductCategory))
        return categories.all()
    
    
async def add_product_category(name: str) -> True | False:
    async with async_session() as session:
        session.add(ProductCategory(name=name))
        await session.commit()
    
    
async def delete_product_category(product_category: ProductCategory):
    async with async_session() as session:
        await session.delete(product_category)
        await session.commit()