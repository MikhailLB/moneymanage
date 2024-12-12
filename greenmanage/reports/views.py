from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from reminders.tasks import download_statistics
from reports.services import generate_excel

@csrf_exempt
def reports_view(request):
    """Рендерит страницу с отчетами и кнопкой для экспорта в Excel."""
    return render(request, 'reports/reports.html')

@csrf_exempt
def export_to_excel(request):
    """Обрабатывает запрос на экспорт файла Excel."""
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    if not start or not end:
        return HttpResponse("Пожалуйста, укажите параметры start_date и end_date.", status=400)

    excel_file = generate_excel(user=request.user, start=start, end=end)
    now = datetime.now()
    date = now.strftime('%Y_%m_%d')

    response = HttpResponse(
        excel_file,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="transactions_{date}.xlsx"'
    download_statistics(user=request.user)
    return response