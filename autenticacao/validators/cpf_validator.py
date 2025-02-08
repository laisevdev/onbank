import re
from django.core.exceptions import ValidationError

def validate_cpf(value):
    cpf = re.sub(r'\D', '', value)

    if not cpf.isdigit() or len(cpf) != 11:
        raise ValidationError("CPF deve conter 11 dígitos.")

    
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido, dígitos iguais")

    
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            raise ValidationError("CPF inválido.")
