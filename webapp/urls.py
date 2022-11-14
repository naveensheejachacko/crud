from . import views
from django.urls import path

urlpatterns = [
    path('',views.user_login,name='login'),
    path('signup/',views.user_signup,name='signup'),
    path('home/',views.home,name='home'),
    path('logout/',views.user_logout,name='logout'),
    path('adminn/',views.admin_login,name='adminn'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('users/',views.users,name='users'),
    path('insert/',views.user_insert,name='insert'),
    path('<int:id>/',views.user_insert, name='update'),
    path('delete/<int:id>/',views.user_delete,name='delete'),
    path('search/',views.search,name='search')
]