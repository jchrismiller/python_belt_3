from __future__ import unicode_literals
from .models import User, Travel
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Sum

def index(request):
	context={
		'users': User.objects.all()
	}
	return render(request, "login_reg/index.html", context)

def registration(request):
	result = User.objects.validate_registration(request.POST)	
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Registration Successful!")
	return redirect('/travels')

def login(request):
	result = User.objects.validate_login(request.POST)
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Login Successful!")
	return redirect('/travels')

def travels(request):
	if 'user_id' not in request.session: #LOOK AT THIS
		return redirect('/')
	current_user = User.objects.get(id = request.session['user_id'])
	context = {
		'current_user': current_user,
		'travel_plans':Travel.objects.all(),
		'trip_schedule':Travel.objects.filter(planned_by=current_user),
		'other_plans':Travel.objects.exclude(planned_by=current_user).all()

# 'users': User.objects.exclude(id = request.session['user_id']), #FIX THIS

	# 	'compliments': Compliment.objects.all(),
	# 	'fav_comps': Compliment.objects.filter(faved_by = current_user).all()
	}	
	return render(request, 'login_reg/travels.html', context) 

def add_page(request):
	if 'user_id' not in request.session:
		return redirect('/')
	current_user = User.objects.get(id = request.session['user_id'])
	return render(request, 'login_reg/add.html')

def destination(request, travel_id):	
	context = {
	'destination_view':Travel.objects.get(id = travel_id),
	'joiners':User.objects.filter(joined = travel_id)
# 		'fav_comps': Compliment.objects.filter(faved_by = current_user).all()
	}
	return render(request, 'login_reg/destination.html', context) 

def add(request):
	if 'user_id' not in request.session:
		return redirect('/')
	current_user = User.objects.get(id = request.session['user_id'])
	Travel.objects.create(
		destination=request.POST['destination'],
		description=request.POST['description'],
		start_date=request.POST['start_date'],
		end_date=request.POST['end_date'],
		planned_by=current_user
		)
	return redirect('/travels')

def join(request, travel_id):
	current_user = User.objects.get(id=request.session['user_id'])
	joined = Travel.objects.get(id = travel_id).joined_by.add(current_user)

	return redirect('/travels')

def favorite(request, comp_id):
	current_user = User.objects.get(id=request.session['user_id'])
	favorite = Compliment.objects.get(id = comp_id).faved_by.add(current_user)

	return redirect('/success')

# def success(request):
# 	if 'user_id' not in request.session: #LOOK AT THIS
# 		return redirect('/')
# 	current_user = User.objects.get(id = request.session['user_id'])
# 	context = {
# 		'current_user': current_user,
# 		'compliments': Compliment.objects.all(),
# 	}	
# 	return render(request, 'login_reg/success.html', context)

def listofcomps(request):
	try:
		request.session['user_id']
	except Keyerror:
		return redirect('/')

	current_user = User.objects.get(id = request.session['user_id'])
	context = {
		'your_comps': Compliment.objects.filter(author=current_user).all(),
		'compliments': Compliment.objects.all()
	}
	print context['your_comps']
	return render(request, 'login_reg/listofcomps.html', context)

def compliment(request):
	try:
		request.session['user_id']
	except Keyerror:
		return redirect('/')
	print 'hello'
	current_user = User.objects.get(id=request.session['user_id'])
	Compliment.objects.create(
		content = request.POST['content'],
		author = current_user)	

	return redirect('/success')

def favorite(request, comp_id):
	current_user = User.objects.get(id=request.session['user_id'])
	favorite = Compliment.objects.get(id = comp_id).faved_by.add(current_user)

	return redirect('/success')

def logout(request, user_id):
	del request.session
	return redirect('/')
