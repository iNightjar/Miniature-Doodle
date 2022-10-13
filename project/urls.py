
from django.contrib import admin
from django.urls import path
from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #1 ordinal route with django
    path('django/jsonresponsenomodel/', views.no_rest_no_model),

    #2 no rest but django, queryset with json response
    path('django/jsonresponsefrommodel/', views.no_rest_from_model)

]
