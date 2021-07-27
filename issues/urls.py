# from issues.models import Issue
from django.urls import path

from issues.views import ProjectIssuesList, ProjectIssuesDetail
from issues.views import CommentList
from issues.views import CommentDetail
urlpatterns = [

    # 11/ Récupérer la liste des problèmes liés à un projet
    # GET /projects/{id}/issues/
    # 12/ Créer un problème dans un projet
    # POST /projects/{id}/issues/
    path('projects/<int:pk>/issues/', ProjectIssuesList.as_view()),

    # 13/ Mettre à jour un problème dans un projet
    # PUT /projects/{id}/issues/{id}
    # 14/ Supprimer un problème d'un projet
    # DELETE /projects/{id}/issues/{id}
    # 15. Créer des commentaires sur un problème
    # POST /projects/{id}/issues/{id}/comments/
    path('projects/<int:pk_project>/issues/<int:pk_issue>/',
         ProjectIssuesDetail.as_view()),

    # 16 Récupérer la liste des commentaires d'un problème
    # GET /projects/{id}/issues/{id}/comments/
    path('projects/<int:pk_project>/issues/<int:pk_issue>/comments/',
         CommentList.as_view()),

    path('projects/<int:pk_project>/issues/<int:pk_issue>/comments/<int:pk_comment>/',
         CommentDetail.as_view())
]
