import asyncio

from sqlalchemy import Integer, BigInteger, ForeignKey, String, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from app.config import DATABASE, ECHO
from typing import List


engine = create_async_engine(url=DATABASE, echo=ECHO)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_tg: Mapped[BigInteger] = mapped_column(BigInteger)
    basket_rel: Mapped[List['Basket']] = relationship(
        back_populates='user_rel')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean)

    item_rel: Mapped[List['Item']] = relationship(
        back_populates='categories_rel')


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    price: Mapped[int] = mapped_column(Integer)
    photo:  Mapped[str] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean)

    category:  Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category_rel: Mapped[Category] = relationship(back_populates='item_rel')
    basket_rel: Mapped[List['Basket']] = relationship(
        back_populates='item_rel')


class Basket(Base):
    __tablename__ = 'baskets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item: Mapped[int] = mapped_column(ForeignKey('items.id'))

    user_rel: Mapped['User'] = relationship(back_populates='basket_rel')
    item_rel: Mapped['Item'] = relationship(back_populates='basket_rel')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(async_main())
