"""Pruebas unitarias de validación de los DTOs (schemas.py)."""
import pytest
from pydantic import ValidationError

from schemas import DtoUserLogin, DtoUserRegister, Role, Student


def test_login_valido_acepta_email_y_password():
    dto = DtoUserLogin(email="ana@kiwi.com", password="Clave123")
    assert dto.email == "ana@kiwi.com"
    assert dto.password == "Clave123"


def test_login_rechaza_email_invalido():
    with pytest.raises(ValidationError):
        DtoUserLogin(email="no-es-un-email", password="Clave123")


def test_login_rechaza_password_menor_a_3_caracteres():
    with pytest.raises(ValidationError):
        DtoUserLogin(email="ana@kiwi.com", password="ab")


def test_login_rechaza_password_mayor_a_16_caracteres():
    with pytest.raises(ValidationError):
        DtoUserLogin(email="ana@kiwi.com", password="x" * 17)


def test_registro_convierte_role_a_enum():
    dto = DtoUserRegister(email="profe@kiwi.com", password="Clave123", role="TEACHER")
    assert dto.role == Role.TEACHER


def test_registro_rechaza_role_inexistente():
    with pytest.raises(ValidationError):
        DtoUserRegister(email="x@kiwi.com", password="Clave123", role="DIRECTOR")


def test_student_inicia_con_monedas_en_cero():
    student = Student(role="STUDENT")
    assert student.coin_earned == 0
    assert student.coin_available == 0
