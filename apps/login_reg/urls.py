from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^logout$', views.index),
	url(r'^add$', views.add),	
	url(r'^add_page$', views.add_page),	
	url(r'^registration$', views.registration),
	url(r'^travels$', views.travels),
	url(r'^destination/(P?\d+)$', views.destination),
	url(r'^join/(P?\d+)$', views.travels),
	url(r'^join$', views.travels),
	# url(r'^listofcomps$', views.listofcomps),
	# url(r'^compliment$', views.compliment),
	# url(r'^favorite$', views.favorite),
	# url(r'^favorite/(P?\d+)$', views.favorite),	
	# url(r'^compliment/(P?\d+)$', views.compliment)
	# url(r'^user/(?P<user_id>\d+)$', views.show)
]