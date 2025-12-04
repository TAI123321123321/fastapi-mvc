from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, relationship

from app.models import enums
from app.models import dto


Base = declarative_base()


employee_skill_table = Table(
    "employee_skills",
    Base.metadata,
    Column(
        "employee_id",
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "skill_id",
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True,),
    Column("level", String, nullable=True),
    Column("created_at",DateTime(),server_default=current_timestamp(),
    ),
)


class UserDb(Base):
    __tablename__ = "users"

    id = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    name = mapped_column("name", String)
    surname = mapped_column("surname", String)
    role = mapped_column("role", Enum(enums.UserRole), default=enums.UserRole.USER)
    email = mapped_column("email", String, unique=True)
    password = mapped_column("password", String)
    updated_at = mapped_column(
        "updated_at",
        DateTime(),
        server_default=current_timestamp(),
        server_onupdate=current_timestamp(),
    )
    created_at = mapped_column(
        "created_at", DateTime(), server_default=current_timestamp()
    )

    # One-to-one: 1 user <-> 1 employee
    employee = relationship(
        "EmployeeDb",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def to_dto(self, include_depat=False) -> dto.UserDTO:
        """Convert this UserDb row into a DTO."""
        return dto.UserDTO(
            id=self.id,
            name=self.name,
            surname=self.surname,
            role=self.role,
            email=self.email,
            updated_at=self.updated_at,
            created_at=self.created_at,
        )


class EmployeeDb(Base):
    """
    Bảng nhân viên (employee) có quan hệ 1-1 với bảng users.
    Mỗi nhân viên bắt buộc gắn với đúng 1 user.
    """

    __tablename__ = "employees"

    id = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )

    # Các thông tin nhân viên cơ bản, bạn có thể bổ sung thêm field tuỳ ý
    code = mapped_column("code", String, unique=True)  # mã nhân viên
    position = mapped_column("position", String, nullable=True)  # chức vụ
    department = mapped_column("department", String, nullable=True)  # phòng ban

    updated_at = mapped_column(
        "updated_at",
        DateTime(),
        server_default=current_timestamp(),
        server_onupdate=current_timestamp(),
    )
    created_at = mapped_column(
        "created_at", DateTime(), server_default=current_timestamp()
    )

    user = relationship("UserDb", back_populates="employee")
    skills = relationship(
        "SkillDb",
        secondary=employee_skill_table,
        back_populates="employees",
    )



class SkillDb(Base):
    __tablename__ = "skills"

    id = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    name = mapped_column("name", String, unique=True, nullable=False)
    description = mapped_column("description", String, nullable=True)
    created_at = mapped_column(
        "created_at", DateTime(), server_default=current_timestamp()
    )
    updated_at = mapped_column(
        "updated_at",
        DateTime(),
        server_default=current_timestamp(),
        server_onupdate=current_timestamp(),
    )

    employees = relationship(
        "EmployeeDb",
        secondary=employee_skill_table,
        back_populates="skills",
    )


# one to one relationship (ví dụ cũ, có thể dùng tương tự EmployeeDb nếu cần)
class TaxAccountDb(Base):
    __tablename__ = "tax_accounts"
    id = mapped_column(
        "id", Integer, ForeignKey("users.id"), index=True, primary_key=True
    )
    rate = mapped_column("rate", Float(precision=2))
    updated_at = mapped_column(
        "updated_at",
        DateTime(),
        server_default=current_timestamp(),
        server_onupdate=current_timestamp(),
    )
    created_at = mapped_column(
        "created_at", DateTime(), server_default=current_timestamp()
    )


# one to many relationship
class SalaryDb(Base):
    __tablename__ = "salaries"
    id = mapped_column("id", Integer(), primary_key=True, autoincrement=True)
    user_id = mapped_column("user_id", Integer(), ForeignKey("users.id"))
    amount = mapped_column("amount", Float(precision=2))
    amount_hours = mapped_column("amount_hours", Float(precision=1))
    salary_date = mapped_column("salary_date", DateTime())
    updated_at = mapped_column(
        "updated_at",
        DateTime(),
        server_default=current_timestamp(),
        server_onupdate=current_timestamp(),
    )
    created_at = mapped_column(
        "created_at", DateTime(), server_default=current_timestamp()
    )