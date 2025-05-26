
from django.contrib import admin
from django.urls import path
from Genie.views import dockerfile_form,generate_output,jenkinsfile_form,terraform_form,ansible_form,k8s_form,github_action_form,home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('dockerfile/', dockerfile_form, name='dockerfile_form'),
    path('jenkinsfile/', jenkinsfile_form, name='jenkinsfile_form'),
    path('terraform/', terraform_form, name='terraform_form'),
    path('ansible/', ansible_form, name='ansible_form'),
    path('k8s/',k8s_form,name='k8s'),
    path('github-action/', github_action_form, name='github_action_form'),
    path('generate/', generate_output, name='generate_output'),
]
