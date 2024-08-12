from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///database.sqlite3')

async_session = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()


class ProductCategory(Base):
    __tablename__ = 'product_categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    
    
class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    category_name: Mapped[str] = mapped_column(ForeignKey('product_categories.name', 
                                                          ondelete='CASCADE'))
    added_by_user_username: Mapped[str] = mapped_column(ForeignKey('users.username',
                                                                   ondelete='CASCADE'))


async def create_database_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)