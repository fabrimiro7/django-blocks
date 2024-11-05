from django.db import models
from django.core.validators import MinLengthValidator

class SingleTestElement(models.Model):
    title = models.CharField(verbose_name="Title", validators=[MinLengthValidator(2)], max_length=250, null=True,
                            blank=True)

    def __str__(self):
            return self.title

    class Meta:
        verbose_name = 'SingleTestElement'
        verbose_name_plural = 'SingleTestElement'
        ordering = ('title',)