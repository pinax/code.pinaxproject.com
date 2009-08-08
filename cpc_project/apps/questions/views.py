from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

from questions.models import Question


def question_list(request, group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404()
    else:
        group = None
    
    questions = Question.objects.all()
    
    if group:
        questions = group.content_objects(questions)
    
    return render_to_response("questions/question_list.html", {
        "group": group,
        "questions": questions,
    }, context_instance=RequestContext(request))


def question_detail(request, question_id, group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404()
    else:
        group = None
    
    questions = Question.objects.all()
    
    if group:
        questions = group.content_objects(questions)
    
    question = get_object_or_404(questions, pk=question_id)
    responses = question.responses.all() # @@@ ordering
    
    if question.user == request.user:
        is_me = True
    else:
        is_me = False
    
    if "accept" in request.GET:
        response_id = int(request.GET["accept"])
        
        if is_me:
            response = responses.get(pk=response_id)
            response.accept()
        else:
            return HttpResponse("cannot perform action")
        
        return HttpResponse("good")
    
    return render_to_response("questions/question_detail.html", {
        "group": group,
        "is_me": is_me,
        "question": question,
        "responses": responses,
    }, context_instance=RequestContext(request))
