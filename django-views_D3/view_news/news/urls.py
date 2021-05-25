###
from django.urls import path
from .views import NewsList    # импортируем наше представление
from .views import NewsDetail  # импортируем наше представление
 
 
urlpatterns = [
    path('',         NewsList.as_view()),   # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', NewsDetail.as_view()), # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
]