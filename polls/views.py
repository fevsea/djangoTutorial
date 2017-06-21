from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views import generic

from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        data = {
            'question': question,
            # Translators: Error when POSt and not aption selected
            'error_message': _("You didn't select a choice."),
        }

        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', data)

    else:
        selected_choice.votes = F('votes') + 1  # F -> No race condition
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# text = ungettext(
#     'There is %(count)d %(name)s available.',
#     'There are %(count)d %(name)s available.',
#     count
# ) % {
#     'count': count,
#     'name': name
# }


def tests(request):
    context = {
        "title": _("tests"),
        "second": "second",
    }
    return render(request, 'polls/tests.html', context)
