import io
from openpyxl import Workbook
from transactions.models import Transaction


def generate_excel(user, start, end):
    wb = Workbook()

    # Получаем транзакции для пользователя за указанный период
    data = Transaction.objects.filter(user=user, created_at__gte=start, created_at__lte=end)

    if not data.exists():  # Проверяем, есть ли транзакции
        ws = wb.active
        ws.title = "No Data"
        ws.append(["Номер", "Дата", "Описание", "Сумма", "Валюта", "Категория", "Тип транзакции"])
    else:
        ws = wb.create_sheet(title="Транзакции")
        ws.append(["Номер", "Дата", "Описание", "Сумма", "Валюта", "Категория", "Тип транзакции"])

        for index, transaction in enumerate(data, start=1):
            ws.append([
                index,  # Номер строки, т.к. pk необязательно идти по порядку
                transaction.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Дата (если поле - DateTimeField)
                transaction.description,  # Описание
                transaction.amount,  # Сумма
                transaction.currency.code,  # Валюта
                transaction.category.name,  # Категория
                transaction.transaction_type.verbose_name  # Тип транзакции
            ])

        # Удаляем автоматический лист "Sheet", если он существует
        if 'Sheet' in wb.sheetnames:
            del wb['Sheet']

    # Сохраняем книгу в буфер
    buffer = io.BytesIO()
    wb.save(buffer)

    # Возвращаем буфер с начала (чтобы его можно было прочитать с начала)
    buffer.seek(0)
    return buffer
