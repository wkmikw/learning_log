from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
	"""docstring for Topic"""
			
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User)

	def __str__(self):
		# return model's str
		return self.text

class Entry(models.Model):
	"""docstring for Entry"""
	topic = models.ForeignKey(Topic)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'entries'

	def __str__(self):
		# return model's str
		if len(self.text) <= 50:
			return self.text
		return self.text[:50] + "..."
			
		