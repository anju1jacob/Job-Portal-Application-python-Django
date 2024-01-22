"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from jobportalapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),


    path("", views.home, name="home"),
    path("registration", views.registration, name="registration"),
    path("about", views.about, name="about"),
    path("contacts", views.contacts, name="contacts"),
    path("joblist", views.joblist, name="joblist"),
    path("loginpage", views.loginpage, name="loginpage"),
    path("logout_user", views.logout_user, name="logout_user"),
    path("forgetpwd", views.forgetpwd, name='forgetpwd'),
    path("passwordreset", views.passwordreset, name="passwordreset"),
    path("reset", views.reset, name="reset"),
    path("update/<int:id>", views.update, name="update"),
    path("subscribe", views.subscribe, name="subscribe"),

# Jobseeker's module urls
    path("jobseeker_register", views.jobseeker_register, name="jobseeker_register"),
    path("jobseeker_home", views.jobseeker_home, name="jobseeker_home"),
    path("jobseeker_changepwd", views.jobseeker_changepwd, name="jobseeker_changepwd"),
    path("jobseeker_profile", views.jobseeker_profile, name="jobseeker_profile"),
    path("jobseeker_view_joblist", views.jobseeker_view_joblist, name="jobseeker_view_joblist"),
    path("jobseeker_jobdetails/<int:id>", views.jobseeker_jobdetails, name="jobseeker_jobdetails"),
    path("jobseeker_applyjob/<int:id>", views.jobseeker_applyjob, name="jobseeker_applyjob.html"),
    path("jobseeker_view_company", views.jobseeker_view_company, name="jobseeker_view_company"),
    path("jobseeker_view_companydetails/<int:id>", views.jobseeker_view_companydetails, name="jobseeker_view_companydetails"),
    path("jobseeker_view_myjoblist", views.jobseeker_view_myjoblist, name="jobseeker_view_myjoblist"),


# Recruiter module urls
    path("recruiter_register", views.recruiter_register, name="recruiter_register"),
    path("recruiter_home", views.recruiter_home, name="recruiter_home"),
    path("recruiter_changepwd", views.recruiter_changepwd, name="recruiter_changepwd"),
    path("recruiter_profile", views.recruiter_profile, name="recruiter_profile"),
    path("recruiter_addcompany", views.recruiter_addcompany, name="recruiter_addcompany"),
    path("recruiter_company", views.recruiter_company, name="recruiter_company"),
    path("recruiter_company_gallery", views.recruiter_company_gallery, name="recruiter_company_gallery"),
    path("recruiter_postjob", views.recruiter_postjob, name="recruiter_postjob"),
    path("recruiter_managejobs", views.recruiter_managejobs, name="recruiter_managejobs"),
    path("recruiter_view_applications", views.recruiter_view_applications, name="recruiter_view_applications"),
    path("recruiter_view_listof_application/<int:id>", views.recruiter_view_listof_application, name="recruiter_view_listof_application"),
    path("recruiter_accept_applicant/<int:id>", views.recruiter_accept_applicant, name="recruiter_accept_applicant"),
    path("recruiter_reject_applicant/<int:id>", views.recruiter_reject_applicant, name="recruiter_reject_applicant"),
    path("recruiter_update_jobpost/<int:id>", views.recruiter_update_jobpost, name="recruiter_update_jobpost"),


# Admin module urls
    path("admin_home", views.admin_home, name="admin_home"),
    path("admin_add_recruiter", views.admin_add_recruiter, name="admin_add_recruiter"),
    path("admin_changepwd", views.admin_changepwd, name="admin_changepwd"),
    path("admin_view_pendingrecruiter", views.admin_view_pendingrecruiter, name="admin_view_pendingrecruiter"),
    path("admin_delete_pendingrecruiter/<int:id>", views.admin_delete_pendingrecruiter, name="admin_delete_pendingrecruiter"),
    path("admin_approve_pendingrecruiter/<int:id>", views.admin_approve_pendingrecruiter, name="admin_approve_pendingrecruiter"),
    path("admin_reject_pendingrecruiter/<int:id>", views.admin_reject_pendingrecruiter, name="admin_reject_pendingrecruiter"),
    path("admin_view_acceptedrecruiter", views.admin_view_acceptedrecruiter, name="admin_view_acceptedrecruiter"),
    path("admin_delete_acceptedrecruiter/<int:id>", views.admin_delete_acceptedrecruiter, name="admin_delete_acceptedrecruiter"),
    path("admin_reject_acceptedrecruiter/<int:id>", views.admin_reject_acceptedrecruiter, name="admin_reject_acceptedrecruiter"),
    path("admin_pending_acceptedrecruiter/<int:id>", views.admin_pending_acceptedrecruiter, name="admin_pending_acceptedrecruiter"),
    path("admin_view_rejectedrecruiter", views.admin_view_rejectedrecruiter, name="admin_view_rejectedrecruiter"),
    path("admin_pending_rejectedrecruiter/<int:id>", views.admin_pending_rejectedrecruiter, name="admin_pending_rejectedrecruiter"),
    path("admin_delete_rejectedrecruiter/<int:id>", views.admin_delete_rejectedrecruiter, name="admin_delete_rejectedrecruiter"),
    path("admin_approve_rejectedrecruiter/<int:id>", views.admin_approve_rejectedrecruiter, name="admin_approve_rejectedrecruiter"),
    path("admin_view_applicants", views.admin_view_applicants, name="admin_view_applicants"),
    path("admin_delete_applicant/<int:id>", views.admin_delete_applicant, name="admin_delete_applicant"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)