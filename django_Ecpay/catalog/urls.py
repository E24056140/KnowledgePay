from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('createOrder/', views.createOrder_view, name='createOrder'),    
    path('itemShow/',views.itemShow_view , name = 'itemShow'),
    path('ecpayReply/',views.ecpayReply_view , name = 'ecpayReply'),
    path('signUp/',views.signUp_view,name = 'signUp'),
    path('addItem/',views.addItem_view,name = 'addItem'),
    path('addItemOK/',views.addItemOK_view,name = 'addItemOK'),
    path('myItem/',views.myItem_view,name = 'myItem'),
    path('update/',views.update_view,name = 'update'),
    path('delete/',views.delete_view,name = 'delete'),
    path('myOrder/',views.myOrder_view,name = 'myOrder'),
    path('orderDetail/',views.orderDetail_view,name = 'orderDetail'),
]