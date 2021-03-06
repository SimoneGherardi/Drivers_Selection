from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.collecting_data_view, name='collecting_data_view'),
    url(r'^showresult/$', views.create_scores_view, name='create_scores_view'),
    url(r'^showscores/$', views.show_scores_view, name='show_scores_view'),
    url(r'^showfinalscores/$', views.show_final_scores_view, name='show_final_scores_view'),
]