from django.urls import path

from projects.views import (ProjectContributorDestroy,
                            ProjectContributorsList, ProjectDetail,
                            ProjectList, RegisterAPI)

urlpatterns = [


    path('signup/', RegisterAPI.as_view()),
    path('projects/', ProjectList.as_view()),
    path('projects/<int:pk>/', ProjectDetail.as_view()),
    path('projects/<int:pk>/users/',
         ProjectContributorsList.as_view()),
    path('projects/<int:pk>/users/<int:pk_user>/',
         ProjectContributorDestroy.as_view()),
]
