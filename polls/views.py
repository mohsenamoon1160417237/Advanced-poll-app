from django.shortcuts import render , get_object_or_404 , redirect
from .models import Choice , Poll , UserVotes
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import PollCreateForm , ChoiceForm , ChoiceFormset




@login_required
@require_POST
def choice(request , choice_id , choice_slug):

	choice = get_object_or_404(Choice , id=choice_id , slug=choice_slug)
	poll = choice.poll
	same_ip = False
	self_vote = None
	same_votes = None

	try:

		same_votes = UserVotes.objects.filter(poll=poll).exclude(user__id=request.user.id)
		self_vote = UserVotes.objects.get(user__id=request.user.id,
										  poll=poll)

	except:

		pass


	if same_votes:

		for vote in same_votes:

			if vote.user_ip == request.META['REMOTE_ADDR']:

				same_ip = True




	if same_ip == False:

		if self_vote == None or self_vote.total < poll.vote_limit:

			try:
				user_vote = UserVotes.objects.get(user__id=request.user.id,
											  	  poll=poll)
				user_vote.total += 1
				user_vote.user_ip = request.META['REMOTE_ADDR']
				user_vote.save()

			except UserVotes.DoesNotExist:

				UserVotes.objects.create(user=request.user,
									 	poll=poll,
									 	user_ip=request.META['REMOTE_ADDR'],
									 	total=1)



			choice.users.add(request.user)
			choice.poll.users.add(request.user)


	return redirect(choice.poll.get_absolute_url())




@login_required
def poll(request , poll_id , poll_slug):

	poll = get_object_or_404(Poll , id=poll_id , slug=poll_slug)
	choices = Choice.objects.filter(poll=poll)
	user_vote = None

	try:
		user_vote = UserVotes.objects.get(user__id=request.user.id,
										  poll=poll)
	except:
		pass

	return render(request , 'poll.html' , {'poll':poll , 
										   'choices': choices,
										   'user_vote':user_vote})




@require_POST
@login_required
def unvote(request , choice_id , choice_slug):

	choice = get_object_or_404(Choice , id=choice_id , slug=choice_slug)
	choice.users.remove(request.user)
	choices = choice.poll.choices.exclude(id=choice.id , slug=choice.slug)
	emptyChoices = 0

	for choice in choices:
		if not request.user in choice.users.all():
			emptyChoices += 1

	if emptyChoices == choices.count():

		choice.poll.users.remove(request.user)

	try:
		user_vote = UserVotes.objects.get(user__id=request.user.id,
						  	  			  poll=choice.poll,
						  	  			  total__gt=1)
		
		user_vote.total -= 1
		user_vote.save()

	except:
		
		user_vote = UserVotes.objects.get(user__id=request.user.id,
										  poll=choice.poll,
										  total=1)
		user_vote.total -= 1
		user_vote.user_ip = None
		user_vote.save()

	return redirect(choice.poll.get_absolute_url())





@login_required
def create_poll(request):

	if request.method == 'POST':

		poll_form = PollCreateForm(files=request.FILES,
							  	   data=request.POST)

		formset = ChoiceFormset(data=request.POST)

		

		if poll_form.is_valid() and formset.is_valid():

			new_poll = poll_form.save(commit=False)
			new_poll.owner = request.user
			new_poll.save()

			for form in formset:

				if form.cleaned_data != {}:
					new_choice = form.save(commit=False)
					new_choice.poll = new_poll
					new_choice.save()

			return redirect('home')

	else:

		poll_form = PollCreateForm()
		formset = ChoiceFormset()

	section = 'create'

	return render(request , 'poll_form.html' , {'poll_form':poll_form,
												'formset':formset,
												'section':section})




#ip = request.META['REMOTE_ADDR']

	
