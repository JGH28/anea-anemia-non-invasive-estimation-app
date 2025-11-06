def interpretar_resultado(valor, sexo="Hombre", edad=None, factor=1.0):
    """
    Interpreta el valor de hemoglobina ajustado por sexo y edad. 
    Usa rangos oficiales para hombre y mujer adultos.
    """
    valor_ajustado = valor * factor

    if valor_ajustado < 4:
        return "Medición no válida", "gray", valor_ajustado

    if sexo.lower() in ["hombre", "masculino"]:
        if valor_ajustado < 8.0:
            return "Anemia severa", "red", valor_ajustado
        elif 8.0 <= valor_ajustado < 10.0:
            return "Anemia moderada", "orange", valor_ajustado
        elif 10.0 <= valor_ajustado < 13.0:
            return "Anemia leve", "yellow", valor_ajustado
        else:
            return "Normal", "green", valor_ajustado

    elif sexo.lower() in ["mujer", "femenino"]:
        if valor_ajustado < 8.0:
            return "Anemia severa", "red", valor_ajustado
        elif 8.0 <= valor_ajustado < 11.0:
            return "Anemia moderada", "orange", valor_ajustado
        elif 11.0 <= valor_ajustado < 12.0:
            return "Anemia leve", "yellow", valor_ajustado
        else:
            return "Normal", "green", valor_ajustado

    return "Categoría no definida", "gray", valor_ajustado