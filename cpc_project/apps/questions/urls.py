from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r'^$', "questions.views.question_list", name="questions_question_list"),
    url(r'^ask/$', "questions.views.question_create", name="questions_question_create"),
    url(r'^question/(?P<question_id>\d+)/$', "questions.views.question_detail", name="questions_question_detail"),
)
