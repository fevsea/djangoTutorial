from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views import generic

from polls.models import Question, Choice


class IndexView(generic.ListView):
    """
       Display all :model:`polls.Questions`.

       **Context**

       ``polls``
           latests_question_list

       **Template:**

       :template:`polls/index.html`
       """
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
    """
       Detalled view of a :model:`polls.Questions`.

       **Context**

       ``polls``
           question

       **Template:**

       :template:`polls/detail.html`
       """
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
    """
       Votes for a :model:`polls.Choice`.

       **Context**

       ``polls``
           question
           error_message

       **Template:**

       :template:`polls/detail.html`
       """
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
    """
       View to make tests with templates


       **Template:**

       :template:`polls/tests.html`
       """
    # template = get_template('polls/tests.html')

    c = {
        "title": _("tests"),
        "second": "second",
        "tt": request,
    }

    return render(request, 'polls/tests.html', c)
