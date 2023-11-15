from enum import Enum


class RolesEnum(str, Enum):
    ADMIN = 'admin'
    DIRECTOR = 'director'
    AUDITOR_RECEIPT = 'auditor_recepit'
    AUDITOR_OFFER = 'auditor_offer'
    AUDITOR_INTERNAL = 'auditor_internal'
    ACCOUNTANT = 'accountant'
    EMPLOYEE = 'employee'
