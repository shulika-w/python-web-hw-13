from datetime import datetime, date

from sqlalchemy import (
    UUID,
    ForeignKey,
    String,
    DateTime,
    Date,
    Boolean,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (
        UniqueConstraint("user_id", "email", name="uix_email"),
        UniqueConstraint("user_id", "phone", name="uix_phone"),
    )
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=text("gen_random_uuid()")
    )
    first_name: Mapped[str] = mapped_column(String(254), nullable=False)
    last_name: Mapped[str] = mapped_column(String(254), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=True)
    phone: Mapped[str] = mapped_column(String(38), nullable=True)
    birthday: Mapped[date] = mapped_column(Date())
    address: Mapped[str] = mapped_column(String(254), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", onupdate="CASCADE")
    )
    user: Mapped["User"] = relationship("User", back_populates="contacts")

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name


class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=text("gen_random_uuid()")
    )
    username: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    avatar: Mapped[str] = mapped_column(String(254), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(1024), nullable=True)
    is_email_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_password_valid: Mapped[bool] = mapped_column(Boolean, default=True)
    contacts: Mapped["Contact"] = relationship("Contact", back_populates="user")
