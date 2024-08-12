from repositories.dependencies import select, schemas, User, async_session


async def add_user(user_to_add: schemas.AddUser):
    async with async_session() as session:
        session.add(User(**user_to_add.model_dump()))
        await session.commit()
        
        
async def get_user(username: str=None, user_id: int=None) -> User | None:
    async with async_session() as session:
        if username:
            user = await session.scalar(select(User).where(User.username == username))
        elif user_id:
            user = await session.scalar(select(User).where(User.id == user_id))
        return user