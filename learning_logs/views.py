from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
	# homepage
	return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
	# show all topics
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	# show one
	topic = Topic.objects.get(id=topic_id)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	#add new topic
	if request.method != 'POST':
		#haven't post date: create new form
		form = TopicForm()
	else:
		# post date, deal with
		form = TopicForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))

	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context) 

@login_required
def new_entry(request, topic_id):
	# add new entry to sp id
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic 
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', 
				args=[topic_id]))

	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context) 

@login_required
def edit_entry(request, entry_id):
	#edit 
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if request.method != 'POST':
		#create form of the entry
		form = EntryForm(instance=entry)
	else:
		#post
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',
				args=[topic.id]))

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context) 
