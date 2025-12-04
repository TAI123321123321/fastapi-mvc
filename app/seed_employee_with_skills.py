from __future__ import annotations

"""
Quick helper script to create a sample employee with skills.

Run with:
    python -m app.seed_employee_with_skills
"""

from sqlalchemy import select

from app.core.db_context import session_maker, create_tables
from app.core.security import bcrypt_hashing
from app.models.db import UserDb, EmployeeDb, SkillDb


def ensure_user(session, email: str) -> UserDb:
    user = session.execute(select(UserDb).where(UserDb.email == email)).scalar_one_or_none()
    if user:
        return user

    user = UserDb(
        name="Nguyen",
        surname="Van A",
        email=email,
        password=bcrypt_hashing.hash("Secret123!"),
    )
    session.add(user)
    session.flush()  # populate user.id
    return user


def ensure_skill(session, name: str, description: str = "") -> SkillDb:
    skill = session.execute(select(SkillDb).where(SkillDb.name == name)).scalar_one_or_none()
    if skill:
        return skill

    skill = SkillDb(name=name, description=description)
    session.add(skill)
    session.flush()
    return skill


def seed():
    create_tables()

    with session_maker() as session:
        user = ensure_user(session, "employee@example.com")

        existing_employee = session.execute(
            select(EmployeeDb).where(EmployeeDb.user_id == user.id)
        ).scalar_one_or_none()
        if existing_employee:
            print(f"Employee for {user.email} already exists with code {existing_employee.code}")
            return

        python_skill = ensure_skill(session, "Python Backend", "Kinh nghiệm phát triển API FastAPI")
        devops_skill = ensure_skill(session, "DevOps", "CI/CD & container orchestration")

        employee = EmployeeDb(
            user_id=user.id,
            code="EMP001",
            position="Senior Backend Developer",
            department="Engineering",
        )
        employee.skills.extend([python_skill, devops_skill])

        session.add(employee)
        session.commit()
        print("Seeded employee EMP001 with skills Python Backend & DevOps.")


if __name__ == "__main__":
    seed()

