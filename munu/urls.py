"""munu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('image_metric1.html',views.images_computation),
    path('paragraph_metric2.html',views.paragraph_computation_metric2),
    path('link_metric3.html',views.link_calculator_metric3),
    path('donofollow_metric4.html',views.donofollow_calculator_metric4),
    path('brokrnlink_metric5.html',views.brokenlink_metric5),
    path('word_density_metric6.html',views.word_density_checker_metric6),
    path('meta_description_metric7.html',views.meta_description_metric7),
    path('header_description_metric8.html',views.HTTP_HEADER_description_metric8),
    path('canonical_tag_metric9.html',views.canonical_tag_metric9),
    path('robots_text_metric10.html',views.robotstext_metric10)


    




]
    





    # Sukanta
    # path('status_code_metric1.html',views.status_code_metric1),
    # path("social_link_metric2.html",views.social_link)
# ]
