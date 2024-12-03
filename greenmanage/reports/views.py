import plotly.express as px
import pandas as pd
import io
import base64

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from transactions.models import Transaction  # Модель транзакций


@login_required
def expenses_by_day(request):
    # Получение данных из модели
    transactions = Transaction.objects.filter(user=request.user)
    if transactions:
        data = pd.DataFrame(list(transactions.values('date', 'amount')))

        # Группировка по дням и суммирование расходов
        data_grouped = data.groupby('date').sum().reset_index()

        # Построение графика с Plotly
        fig = px.line(data_grouped, x='date', y='amount',
                      title='Expenses by Day',
                      labels={'date': 'Date', 'amount': 'Total Expenses'},
                      template='plotly_dark')

        fig.update_layout(
            title_font_size=24,
            xaxis_title='Date',
            yaxis_title='Expenses',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )

        # Конвертация графика в HTML
        graph_div = fig.to_html(full_html=False)

        return render(request, 'reports/reports.html', {'graph': graph_div})
    else:
        return render(request, 'reports/reports.html')