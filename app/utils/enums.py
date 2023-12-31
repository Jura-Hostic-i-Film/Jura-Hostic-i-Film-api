from enum import Enum


class RolesEnum(str, Enum):
    ADMIN = 'admin'
    DIRECTOR = 'director'
    AUDITOR = 'auditor'
    ACCOUNTANT_RECEIPT = 'accountant_receipt'
    ACCOUNTANT_OFFER = 'accountant_offer'
    ACCOUNTANT_INTERNAL = 'accountant_internal'
    EMPLOYEE = 'employee'
