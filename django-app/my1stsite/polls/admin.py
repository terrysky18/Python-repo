from django.contrib import admin

# Register your models here.
# from djangoproject.com tutorial
# add Question model to have the admin interface shown in the web app

from .models import Question, Choice

# class ChoiceInline(admin.StackedInline):	# Stacked inline display
class ChoiceInline(admin.TabularInline):	# Table inline display
	model = Choice
	extra = 3	# provides fields to add 3 choices

class QuestionAdmin(admin.ModelAdmin):
	# this re-orders the edit form on admin page
	# first element of each tuple is the title of the fieldset
	fieldsets = [
		("The Question", {"fields": ["question_text"]}),
		("Date information", {"fields": ["pub_date"],\
							"classes": ["collapse"]}),
		]
	# Choice objects are edited on Question admin page
	inlines = [ChoiceInline]
	
	# customise the admin change list
	list_display = ("question_text", "pub_date", "was_published_recently")
	list_filter = ["pub_date"]	# filter option automatically generated for DateTimeField
	search_fields = ["question_text"]

# create a model admin object, pass it as 2nd argument
# to customise the admin page
admin.site.register(Question, QuestionAdmin)

# register the choices to answer the question
# this is a basic but inefficient way
#from .models import Choice, Question
#admin.site.register(Choice)

