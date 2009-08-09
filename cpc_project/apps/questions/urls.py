from django.conf.urls.defaults import *
from questions.models import Question, Response
from voting.views import vote_on_object



urlpatterns = patterns("",
    url(r'^$', "questions.views.question_list", name="questions_question_list"),
    url(r'^ask/$', "questions.views.question_create", name="questions_question_create"),
    url(r'^question/(?P<question_id>\d+)/$', "questions.views.question_detail", name="questions_question_detail"),
    url(r'^question/(?P<question_id>\d+)/accept/(?P<response_id>\d+)/$', "questions.views.mark_accepted", name="questions_mark_accepted"),

    # Response voting
    url(r'^question/vote/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/$',
        vote_on_object, dict(
            model=Response,
            template_object_name='object',
            template_name='questions/confirm_vote.html',
            allow_xmlhttprequest=True),
        name="questions_response_vote"),
)
