import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    """
        Sotres a question with severals :model:`polls.Choice`
    """
    question_text = models.CharField(verbose_name=_('question text'), max_length=200, help_text=_("I'm a help text"))
    pub_date = models.DateTimeField(_('date published'))

    def was_published_recently(self):
        """
        Sets if was published in the last day
        :return:
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = _('Published recently?')
    was_published_recently.alters_data = False  # Use when True applies

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')


class Choice(models.Model):
    """
        Represents a possible aswer for a :model:`poll.Question` and their votes
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(_("option"), max_length=200)
    votes = models.IntegerField(_("votes"), default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = _('choice')
        verbose_name_plural = _('choices')
