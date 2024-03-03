# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.fetch_projects, name="projects"),
# ]

from django.urls import path
from . import views

app_name = 'gfi'  # Add this line for namespaced URLs

urlpatterns = [
    path('', views.fetch_projects, name='list_repositories'),  # Update this path
    path('<str:username>/<str:repo_name>/', views.github_repo_details, name='repository_details'),
]
