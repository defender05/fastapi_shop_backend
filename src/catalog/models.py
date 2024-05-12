import datetime
from typing_extensions import Annotated
from sqlalchemy import MetaData, String, Boolean, ForeignKey, TIMESTAMP, LargeBinary, DATE, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint, ForeignKeyConstraint

from ..database import Base
try:
    from src.users.models import UserModel
except ImportError:
    pass

class CategoryModel(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey(
        'categories.id',
        onupdate="CASCADE",
        ondelete="CASCADE",), nullable=True
    )
    parent: Mapped["CategoryModel"] = relationship(
        "CategoryModel",
        remote_side=[id]
    )
    products: Mapped[list["ProductModel"]] = relationship(
        back_populates="category",
        uselist=True,
    )

class ProductModel(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    discount_price: Mapped[float] = mapped_column(nullable=True)
    remaining_stock: Mapped[int] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey(
        'categories.id',
        onupdate="CASCADE",
        ondelete="CASCADE"), nullable=False)

    category: Mapped[CategoryModel] = relationship(
        back_populates="products",
        uselist=False,
        foreign_keys=[category_id]
    )

    cart_item: Mapped[list["CartItemModel"]] = relationship(
        back_populates="product",
        uselist=True,
    )
    order_items: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="product",
        uselist=True,
    )

    # __table_args__ = (UniqueConstraint('sku', name='_sku_uc'),)


class CartItemModel(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    cart_id: Mapped[str] = mapped_column(
        ForeignKey('carts.id', onupdate="CASCADE", ondelete="CASCADE")
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey('products.id', onupdate="CASCADE", ondelete="CASCADE")
    )

    quantity: Mapped[int] = mapped_column(nullable=False)

    cart: Mapped["CartModel"] = relationship(
        back_populates="cart_items",
        uselist=False,
        foreign_keys=[cart_id]
    )
    product: Mapped[ProductModel] = relationship(
        back_populates="cart_item",
        uselist=False,
        foreign_keys=[product_id]
    )


class CartModel(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")
    )

    cart_items: Mapped[list[CartItemModel]] = relationship(
        back_populates="cart",
        uselist=True
    )
    user: Mapped["UserModel"] = relationship(
        back_populates="cart",
        uselist=False,
        foreign_keys=[user_id]
    )


class OrderItemModel(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(
        ForeignKey('orders.id', onupdate="CASCADE", ondelete="CASCADE")
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey('products.id', onupdate="CASCADE", ondelete="CASCADE")
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)  # Цена на момент покупки

    order: Mapped["OrderModel"] = relationship(
        back_populates="order_items",
        uselist=False,
        foreign_keys=[order_id]
    )
    product: Mapped[ProductModel] = relationship(
        back_populates="order_items",
        uselist=False,
        foreign_keys=[product_id]
    )


class OrderModel(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    order_items: Mapped[list[OrderItemModel]] = relationship(back_populates="order", uselist=True)

