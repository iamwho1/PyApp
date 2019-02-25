from django.conf.urls import url
from ProcessApp.views import HomePageView, StackPageView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='process'),
    url('stack/', StackPageView.as_view(), name='stack'),]