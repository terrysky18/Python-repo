from django.shortcuts import render

# base directory\polls\views.py
# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Question

# Each view is responsible for returning an HttpResponse object containing
# the content for the request page or an exception like HTTP404

# each view is written as a function
def index(request):
	latest_question_list = Question.objects.order_by("-pub_date")[:5]
	template = loader.get_template("polls/index.html")
	# context is a dictionary mapping template variable names to Python objects
	context = RequestContext(request, {
		"latest_question_list": latest_question_list,})
	return HttpResponse(template.render(context))
	
	#return HttpResponse("Hello, world.  You're at the polls index.")

def detail(request, question_id):
	return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)
