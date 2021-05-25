###from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import DetailView  # импортируем класс получения деталей объекта
from .models import News
import datetime

 
class NewsList(ListView):
    model = News                 # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news' # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    queryset = News.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.now()  # добавим переменную текущей даты time_now
        ###context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context	

		
# создаём представление в котором будет детали конкретного отдельного товара
class NewsDetail(DetailView):
    model = News                 # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'news_detail.html'   # название шаблона будет new.html
    context_object_name = 'news_detail'  # название объекта. в нём будет
