from django.db import models
from common.models import CommonModel, Person, Places


class Message(CommonModel):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class File(CommonModel):
    uploader = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='uploaded_files')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
