from django.urls import path
import api.views
import logging

urlpatterns = [
    path('', api.views.main),
    path('query/', api.views.query)
]
