from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

# URLPattern = [
#     path('',views.store, name="store"),
#     path('cart/',views.store, name="store"),
#     path('checkout',views.store, name="store"),
# ]
urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('thankyou/', views.thankYou, name="thankyou"),
]