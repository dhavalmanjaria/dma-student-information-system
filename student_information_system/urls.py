"""student_information_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
<<<<<<< HEAD
=======
from django.views.generic.base import TemplateView
>>>>>>> 43d358a9a56880351ce932aa6aeb993dfde1e6fe

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

urlpatterns += [
<<<<<<< HEAD
=======
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index')
]

urlpatterns += [
>>>>>>> 43d358a9a56880351ce932aa6aeb993dfde1e6fe
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    url(r'^user_management/', include('user_management.urls'))
]
<<<<<<< HEAD
=======


# # Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> 43d358a9a56880351ce932aa6aeb993dfde1e6fe
