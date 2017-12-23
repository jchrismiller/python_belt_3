from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
	def validate_login(self, post_data):
		errors = []
		# check DB for post_data['email']
		print post_data
		if len(self.filter(username=post_data['username'])) > 0:
			# check this user's password
			user = self.filter(username=post_data['username'])[0]
			if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
				errors.append('username/password incorrect')
		else:
			errors.append('username/password incorrect')

		if errors:
			return errors
		return user

	def validate_registration(self, post_data):
		errors = []
		# check length of name fields
		if len(post_data['name']) < 3 or len(post_data['username']) < 3:
			errors.append("name fields must be at least 3 characters")
		# check length of name password
		if len(post_data['password']) <8:
			errors.append("password must be at least 8 characters")
		# check name fields for letter characters
		if not re.match(NAME_REGEX, post_data['name']):
			errors.append("name fields must be letter characters only")
		# check uniquness of username


		# check emailness of email
		# if not re.match(EMAIL_REGEX, post_data['email']):
		# 	errors.append("invalid email")
		# check uniquness of email
		# if len(User.objects.filter(username=post_data['username'])) > 0:
		#  	errors.append("username already in use")
		# check password == password confirm
		if post_data['password'] != post_data['confirm_password']:
			errors.append("passwords do not match")

		# if post_data['robot'] != post_data['True']:
		# 	errors.append("No robots allowed!")

		if not errors:
			# make our new user
			# hash password
			hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

			new_user = self.create(
				name=post_data['name'],
				username=post_data['username'],
				password = hashed
			)
			return new_user
		return errors

class TravelManager(models.Manager):
	def validate(self, post_data):
		pass
		# no empty entries
		# travel dates should be future-dated
		# start should be before end


		new_travel = self.create(
			destination=post_data['destination'],
			description=post_data['description'],
			start_date=post_data['start_date'],
			end_date=post_data['end_date'],
			planned_by=user,
			joined_by = ""
				)
		return new_travel

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	# address = models.CharField(max_length=255)
	# credit_card = models.CharField(max_length=30)
	# trader = models.ManyToManyField("User", through = "Gallon")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()

	def __repr__(self):
		return "<User: {} {} {} {} {}>".format(self.id, self.first_name, self.last_name, self.email, self.password)

class Travel(models.Model):
	destination = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	planned_by = models.ForeignKey(User, related_name='plans')
	joined_by = models.ManyToManyField(User, related_name='joined')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)	

	objects = TravelManager()

def __repr__(self):
 		return "<Travel: {} {} {} {} {}>".format(self.destination, self.description, self.start_date, self.end_date, self.planned_by)
# class Compliment(models.Model):
# 	content = models.CharField(max_length=255)
# 	author = models.ForeignKey(User, related_name = 'compliments')
# 	faved_by = models.ManyToManyField(User, related_name= 'favorited')
# 	created_at = models.DateTimeField(auto_now_add = True)
# 	updated_at = models.DateTimeField(auto_now = True)

# 	objects = ComplimentManager()

# 	def __repr__(self):
# 		return "<Compliment: {} {}>".format(self.id, self.author, self.faved_by)

# class ComplimentManager(models.Manager):
# 	def validate(self, data):
# 		pass
# 		# errors = []
# 		# # check length of name comment field
# 		# if len(post_data['content']) < 2:
# 		# 	errors.append("Come on bruh, put some effort into it!")
# 		# if not errors:
# 	def create_compliment(self, post_data, user):
# 			return self.create(
# 					content=post_data['content'],
# 					author = user,
# 					faved_by = ""
# 				)