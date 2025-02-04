from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def add(x, y):
    # Esegui una somma
    return x + y


@shared_task
def stampa(x):
    # Esegui una stampa
    return x


