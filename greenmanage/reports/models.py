from django.contrib.auth import get_user_model
from django.db import models

class Reports(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)  # Название файла
    download_time = models.DateTimeField(auto_now_add=True)  # Время скачивания
    file_path = models.FilePathField(path="downloads/")

    def __str__(self):
        return f"{self.file_name} - {self.download_time} - {self.file_path} - {self.user}"