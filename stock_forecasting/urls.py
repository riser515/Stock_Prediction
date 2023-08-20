from django.contrib import admin
from django.urls import path
from predict_stock.views import stock_predict, index, show_predictions

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('predict/<str:ticker_symbol>/', show_predictions, name='show_predictions')
]
