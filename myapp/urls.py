from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('instructor/',views.instructor,name='instructor'),
    path('course/',views.course,name='course'),
    path('blog-single/<int:pk>',views.blog_single,name='blog-single'),
    path('instructor-details/<int:pk>/',views.instructor_details,name='instructor-details'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('change-password/',views.change_password,name='change-password'),
    path('logout/',views.logout,name='logout'),
    path('artist-index/',views.artist_index,name='artist-index'),
    path('singer/',views.singer,name='singer'),
    path('standup/',views.standup,name='standup'),
    path('dancer/',views.dancer,name='dancer'),
    path('influencer/',views.influencer,name='influencer'),
    path('photographer/',views.photographer,name='photographer'),
    path('writer/',views.writer,name='writer'),
    path('artist-details/',views.artist_details,name='artist-details'),
    path('artist-profile/',views.artist_profile,name='artist-profile'),
    path('artist-edit-details/<int:pk>/',views.artist_edit_details,name='artist-edit-details'),
    path('pay/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
    path('booking/',views.booking,name="booking"),
    path('book/<int:pk>/',views.book,name='book'),
    path('mybook/',views.mybook,name='mybook'),
    path('odered/',views.odered,name='odered'),
    path('contact-me/',views.contact_me,name='contact-me'),
    path('ajax/validate_email/',views.validate_email,name='validate_email'),
    
]
