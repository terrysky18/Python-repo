import datetime
from django.db import models
from django.utils import timezone

# Models from Django project tutorial
# Two models are created, Question and Choice

# Each class is a subclass of django.db.models.Model

class Question(models.Model):
	# contains a question and a publication date
	question_text = models.CharField(max_length=200)
	# pub_date's human-readable name = "date published"
	pub_date = models.DateTimeField("date published")

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() -\
				datetime.timedelta(days=1)
	was_published_recently.admin_order_field = "pub_date"
	was_published_recently.boolenan = True
	was_published_recently.short_description = "Published recently?"

class Choice(models.Model):
	# contains text of the choice and a vote tally
	# each Choice is associated with a Question
	question = models.ForeignKey(Question)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text

