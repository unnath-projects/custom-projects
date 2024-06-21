from django.urls import path
from translator import views
from translator.views import text_input_view

app_name = 'translator'

urlpatterns = [
    path('', views.text_input_view, name='text_input_view'),
]

#path('', views.main_page, name='main_page')