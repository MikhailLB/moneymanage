from datetime import datetime
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.core.files.storage import FileSystemStorage
from reports.models import Reports
from transactions.models import Transaction  # Модель транзакций


def export_to_excel(request, *args, **kwargs):
    export_success = False
    export_error = False

    if request.method == 'GET':
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            # Преобразуем строки в формат datetime
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Запрос данных из базы
            queryset = Transaction.objects.filter(user=request.user, date__gte=start_date, date__lte=end_date)
            data = pd.DataFrame(list(queryset.values()))  # Преобразуем queryset в DataFrame

            # Генерация имени файла
            file_name = f'отчет_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'

            # Сохраняем файл на сервере с помощью FileSystemStorage
            fs = FileSystemStorage(location='downloads')  # Путь для сохранения
            file_path = fs.save(file_name, content=None)  # Сохраняем с использованием FileSystemStorage

            # Получаем полный путь файла
            full_path = fs.path(file_path)  # Получаем полный путь к файлу

            # Проверяем, существует ли файл по этому пути
            if full_path is None:
                raise Exception("Файл не был сохранен, путь пуст")

            # Используем ExcelWriter для записи данных в файл
            with pd.ExcelWriter(full_path, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False)

            # Создаем запись в базе данных для отчета
            Reports.objects.create(file_name=file_name, file_path=full_path, user=request.user)

            # Отправляем файл в ответ
            with open(full_path, 'rb') as f:
                response = HttpResponse(f.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'

                # Устанавливаем флаг успешного экспорта
                export_success = True
                return response

        except Exception as e:
            print(f"Ошибка экспорта данных: {e}")
            export_error = True

    # Рендерим страницу с формой для ввода дат и статусом операции
    return render(request, 'reports/reports.html', {
        'export_success': export_success,
        'export_error': export_error
    })
