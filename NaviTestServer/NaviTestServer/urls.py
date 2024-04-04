"""
URL configuration for NaviTestServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from NaviTestServer.views import *

router = DefaultRouter()
router.register("nodes",Nodes,basename="nodes")
router.register("floors",Floors,basename="floors")
router.register("navigate",Navigate,basename="navigate")
router.register("points",Points,basename="points")
router.register("areas",Areas,basename="areas")

nodes_urlpatterns = [path("", include(router.urls))]

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=nodes_urlpatterns
