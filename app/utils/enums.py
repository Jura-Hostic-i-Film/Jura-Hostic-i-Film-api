from enum import Enum


class RolesEnum(str, Enum):
    ADMIN = 'admin'
    DIRECTOR = 'director'
    AUDITOR = 'auditor'
    ACCOUNTANT = 'accountant'
    EMPLOYEE = 'employee'
