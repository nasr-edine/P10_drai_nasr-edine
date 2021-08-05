from django.urls import path

from projects.views import ProjectList
from projects.views import ProjectDetail
from projects.views import RegisterAPI
from projects.views import ProjectContributorsList

from projects.views import ProjectContributorsList2, ProjectContributorDestroy

urlpatterns = [


    # 1/ Inscription de l'utilisateur
    path('signup/', RegisterAPI.as_view()),

    # 3/ Récupérer la liste de tous les projets d'un utilisateur connecté
    # 4/ Créer un projet
    path('projects/', ProjectList.as_view()),

    # 5/ Récupérer les détails d'un projet via son id
    # 6/ Mettre à jour un projet
    # 7/ Supprimer un projet et ses problèmes
    path('projects/<int:pk>/', ProjectDetail.as_view()),


    # 8/ Ajouter un utilisateur (collaborateur) à un projet
    # 9/ Récupérer la liste de tous les utilisateurs d'un projet
    path('projects/<int:pk>/users/', ProjectContributorsList.as_view()),
    path('projects/<int:pk>/users2/',
         ProjectContributorsList2.as_view()),

    # 10/ Supprimer un utilisateur d'un projet
    path('projects/<int:pk>/users/<int:pk_user>/',
         ProjectContributorDestroy.as_view()),



    # path('users/<int:pk>/', UserDetail.as_view())
]
