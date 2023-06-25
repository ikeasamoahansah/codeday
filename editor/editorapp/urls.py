from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('new_note/', views.post_content, name="post"),
    path('new_snip/', views.post_snip, name="post-snip"),
    path('note/<int:pk>/', views.post_view, name="post-view"),
    path('note/edit/<int:pk>/', views.edit_note, name="edit-note"),
    path('note/snippet/edit/<int:pk>/', views.edit_snippet, name="edit-snippet"),

]
