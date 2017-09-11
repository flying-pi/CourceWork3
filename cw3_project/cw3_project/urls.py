"""cw3_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

from cw3.urls import urlpatterns as cw3_urlpatterns

# url(r'^api/', include(router.urls, namespace='api')),

urlpatterns = [
    # url(r'^', include('cw3.urls')),
    url(r'^admin/', admin.site.urls),
    # url(r'^api/', include('cw3.urls')),
    url(r'^api/', include(cw3_urlpatterns, namespace='api')),
    url(r'^docs/', include_docs_urls(title='My API title')),
]
