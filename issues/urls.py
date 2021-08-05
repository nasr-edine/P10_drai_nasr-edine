# from issues.models import Issue
from django.urls import path

from issues.views import ProjectIssuesList, ProjectIssuesDetail, ProjectIssuesList2, ProjectIssuesDetail2
from issues.views import CommentList, CommentList2, CommentDetail2
from issues.views import CommentDetail
urlpatterns = [


    path('projects/<int:pk_project>/issues2/', ProjectIssuesList2.as_view()),
    path('projects/<int:pk_project>/issues2/<int:pk>/',
         ProjectIssuesDetail2.as_view()),


    path('projects/<int:pk_project>/issues/<int:pk_issue>/comments2/',
         CommentList2.as_view()),
    path('projects/<int:pk_project>/issues/<int:pk_issue>/comments2/<int:pk>/',
         CommentDetail2.as_view()),

    # **********************************************************************************


    path('projects/<int:pk>/issues/', ProjectIssuesList.as_view()),
    path('projects/<int:pk_project>/issues/<int:pk_issue>/',
         ProjectIssuesDetail.as_view()),

    path('projects/<int:pk_project>/issues/<int:pk_issue>/comments/',
         CommentList.as_view()),
    path('projects/<int:pk_project>/issues/<int:pk_issue>/comments/<int:pk_comment>/',
         CommentDetail.as_view())
]
