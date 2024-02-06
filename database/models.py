from config.bot_config import load_config
from sqlalchemy import create_engine, BigInteger, TEXT, ForeignKey
from sqlalchemy.orm import (mapped_column, DeclarativeBase, 
                            Mapped, sessionmaker, relationship)

config = load_config()
engine = create_engine(
    url=f"postgresql+psycopg://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}",
    echo=False
)
session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = 'users'

    user_id = mapped_column(BigInteger, unique=True, primary_key=True)
    name = mapped_column(TEXT)
    surname = mapped_column(TEXT)
    email = mapped_column(TEXT)

    cart: Mapped[list["ShoppingCartModel"]] = relationship(back_populates="user", uselist=True)


class GoodsModel(Base):
    __tablename__ = 'goods'

    good_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category = mapped_column(TEXT)
    title = mapped_column(TEXT)
    author = mapped_column(TEXT)
    description = mapped_column(TEXT)
    price: Mapped[int]
    value: Mapped[int]


class ShoppingCartModel(Base):
    __tablename__ = 'cart'

    cart_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    good_id: Mapped[int]
    good_title: Mapped[str]
    good_value: Mapped[int]
    total_sum: Mapped[int]

    user_fk:Mapped[int]  = mapped_column(ForeignKey('users.user_id'))
    user: Mapped["UserModel"] = relationship(back_populates='cart', uselist=False)


class OrdersModel(Base):
    __tablename__ = 'orders'

    order_id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger, unique=True)

