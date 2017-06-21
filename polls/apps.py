from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _, pgettext_lazy


class PollsConfig(AppConfig):
    name = 'polls'
    verbose_name = pgettext_lazy('app name', 'polls')