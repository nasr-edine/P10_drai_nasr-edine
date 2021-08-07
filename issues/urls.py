from django.urls import path

from issues.views import (CommentDetail, CommentList, ProjectIssuesDetail,
                          ProjectIssuesList)

urlpatterns = [


    path('projects/<int:pk_project>/issues/', ProjectIssuesList.as_view()),
    path('projects/<int:pk_project>/issues/<int:pk>/',
         ProjectIssuesDetail.as_view()),
    path('projects/<int:pk_project>/issues/<int:pk_issue>/comments/',
         CommentList.as_view()),
    path('projects/<int:pk_project>/issues/<int:pk_issue>/comments/<int:pk>/',
         CommentDetail.as_view())
]
