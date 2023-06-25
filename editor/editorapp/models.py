from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import User

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


# Create your models here.


class Note(models.Model):
    title = models.CharField(blank=False, max_length=32)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'
    

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    context = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{self.title}'