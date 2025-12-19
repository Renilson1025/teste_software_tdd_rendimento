from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Union

Money = Decimal
Number = Union[int, float, str, Decimal]


INSS_ALIQUOTA = Decimal("0.08")
INSS_TETO = Decimal("500.00")

IRRF_ISENCAO_ATE = Decimal("2000.00")
IRRF_ALIQUOTA = Decimal("0.10")

MOEDA_2_CASAS = Decimal("0.01")


def calcular_salario_liquido(salario_bruto: Number) -> float:
    bruto = _validar_e_converter_salario(salario_bruto)

    inss = _calcular_inss(bruto)
    irrf = _calcular_irrf(bruto)

    liquido = bruto - inss - irrf
    liquido = _arredondar_moeda(liquido)

    return float(liquido)


def _validar_e_converter_salario(salario_bruto: Number) -> Money:
    bruto = _to_decimal(salario_bruto)
    if bruto <= 0:
        raise ValueError("Salário bruto deve ser maior que zero.")
    return bruto


def _calcular_inss(bruto: Money) -> Money:
    desconto = bruto * INSS_ALIQUOTA
    return min(desconto, INSS_TETO)


def _calcular_irrf(bruto: Money) -> Money:
    if bruto <= IRRF_ISENCAO_ATE:
        return Decimal("0")
    return bruto * IRRF_ALIQUOTA


def _arredondar_moeda(valor: Money) -> Money:
    return valor.quantize(MOEDA_2_CASAS, rounding=ROUND_HALF_UP)


def _to_decimal(valor: Number) -> Money:
    # str() evita problemas clássicos de binário->decimal com float
    return valor if isinstance(valor, Decimal) else Decimal(str(valor))
