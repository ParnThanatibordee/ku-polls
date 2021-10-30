"""Website view function."""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
logger = logging.getLogger("polls")


class IndexView(generic.ListView):
    """Index view method."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


def detail_view(request, pk):
    """Detail view method."""

    user = request.user
    question = get_object_or_404(Question, pk=pk)
    error_message = "Poll can't vote in this time"
    another_user_vote = list(Vote.objects.filter(user=user).filter(choice__question=question))
    if len(another_user_vote) > 0:
        latest_vote_choice = another_user_vote[-1].choice

    if question.can_vote():
        return render(request, 'polls/detail.html', {'question': question, 'latest_vote_choice': latest_vote_choice})
    else:
        return render(request, 'polls/index.html', {'error_message': error_message,
                                                    'latest_question_list': Question.objects.filter(
                                                        pub_date__lte=timezone.now()).order_by('-pub_date')[:5]})


class ResultsView(generic.DetailView):
    """Result view method."""

    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Vote method."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        user = request.user
        all_vote = []
        for choice in question.choice_set.all():
            for vote in choice.vote_set.all():
                all_vote.append(vote)
        another_user_vote = list(Vote.objects.filter(user=user).filter(choice__question=question))
        if len(another_user_vote) > 0:
            if another_user_vote[-1] in all_vote:
                another_user_vote[-1].delete()
        vote = Vote(user=user, choice=selected_choice)
        vote.save()
        vote_event(request, question)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def login_event(request, **kwargs):
    user = request.user
    logger.info(f'{user}(ip:{get_client_ip(request)}) has a login to the polls.')


@receiver(user_logged_out)
def logout_event(request, **kwargs):
    user = request.user
    logger.info(f'{user}(ip:{get_client_ip(request)}) has been logout.')


@receiver(user_login_failed)
def unsuccessful_login_event(request, **kwargs):
    logger.warning(f'A user has failed to login.')


def vote_event(request, question):
    user = request.user
    logger.info(f'{user}(ip:{get_client_ip(request)}) has a vote for a question "{question}".')
