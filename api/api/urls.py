from django.urls import path
import api.views
import logging

urlpatterns = [
    path('', api.views.main),
    path('select/', api.views.select),
    path('update/', api.views.update),
    path('delete/', api.views.delete),
    path('insert/', api.views.insert),
    path('query/', api.views.query)
]
