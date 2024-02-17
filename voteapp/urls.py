from django.urls import path
from voteapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('<user_username>/dashboard/', views.dashboard, name='dashboard'),
    path('<user_username>/vote/', views.vote_view, name='vote'),
    path('submit_vote/', views.submit_vote, name='submit_vote'),

    path('<user_username>/result/', views.result_view, name='result'),
    path('<user_username>/result/winners/', views.winners_view, name='winners'),
    path('<user_username>/profile/', views.profile_view, name='profile'),
    path('<user_username>/profile/edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('<user_id>/profile/edit_profile/crop_image/', views.crop_image_view, name='crop_image'),

    path('<user_username>/profile/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), name='password_change_done'),
    path('<user_username>/profile/password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), name='password_change'),
]
