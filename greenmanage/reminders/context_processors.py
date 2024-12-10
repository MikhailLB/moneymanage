from reminders.models import Reminders  # Модель уведомлений


def user_notifications(request):
    # Проверяем, аутентифицирован ли пользователь
    if request.user.is_authenticated:
        # Получаем количество непрочитанных уведомлений
        unread_notifications = Reminders.objects.filter(user=request.user).count()
    else:
        unread_notifications = 0

    # Возвращаем данные в виде словаря
    return {
        'unread_notifications': unread_notifications,
        'user': request.user,
    }