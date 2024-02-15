from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views
from voteapp import views as view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('voteapp.urls')),
    path('v/', include('voteapp.urls')),

    path('', view.index, name='index'),
    path('register', views.registration_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_change_form.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),
    
]


urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)