from django import forms

class CustomDateInput(forms.DateInput):
    """
    Widget de input de data que garante que o formato de valor seja
    compatível com o HTML5 (YYYY-MM-DD), mesmo quando a validação falha
    em outros campos.
    """
    input_type = 'date'

    def format_value(self, value):
        if value:
            # Converte o objeto date para a string 'YYYY-MM-DD'
            return value.strftime('%Y-%m-%d')
        return super().format_value(value)

class CustomDateTimeInput(forms.DateTimeInput):
    """
    Widget de input de data e hora que garante que o formato de valor seja
    compatível com o HTML5 (YYYY-MM-DDTHH:MM), mesmo quando a validação falha
    em outros campos.
    """
    input_type = 'datetime-local'

    def format_value(self, value):
        if value:
            # Converte o objeto datetime para a string 'YYYY-MM-DDTHH:MM'
            print('olha a datetime como esta:::::::::::::::')
            print(value.strftime('%Y-%m-%dT%H:%M'))
            return value.strftime('YYYY-MM-DDTHH:MM')
        return super().format_value(value)

