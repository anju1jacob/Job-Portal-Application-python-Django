from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    usertype = models.CharField(max_length=20)

class jobseeker(models.Model):
    emp_id =models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    image = models.ImageField(upload_to='Jobseeker profile/')


class recruiter(models.Model):
    recruiter_id =models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    image = models.ImageField(upload_to='Recruiter profile/')
    companyname= models.CharField(max_length=60)
    position=models.CharField(max_length=30)
    status=models.CharField(max_length=30,default=False)

class company(models.Model):
    company_id=models.ForeignKey(recruiter, on_delete=models.CASCADE)
    logo=models.ImageField(upload_to='Company logo/')
    company_type=models.CharField(max_length=30)
    about=models.TextField()
    est_date=models.DateField(null=True)
    city=models.CharField(max_length=70, null=True, blank=True)
    state=models.CharField(max_length=70,null=True, blank=True)
    company_phn=models.IntegerField()
    company_email=models.EmailField()

class company_gallery(models.Model):
    recruiter_imgid=models.ForeignKey(recruiter, on_delete=models.CASCADE)
    company_imgid=models.ForeignKey(company, on_delete=models.CASCADE)
    companyimage = models.ImageField(upload_to='Company gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class job(models.Model):
    JOB_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
        
        # Add other types as needed
    )
     
    job_id=models.ForeignKey(recruiter, on_delete=models.CASCADE)
    job_compid=models.ForeignKey(company, on_delete=models.CASCADE)
    title=models.CharField(max_length=20)
    salary=models.PositiveIntegerField()
    description=models.CharField(max_length=300)
    ideal_candidate=models.CharField(max_length=300)
    experience=models.CharField(max_length=200)
    location=models.CharField(max_length=30)
    vaccancy=models.IntegerField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    startdate=models.DateTimeField(auto_now_add=True, null=True)
    enddate=models.DateField()
    is_available=models.BooleanField(default=True)

   
class apply(models.Model):
    status_choices=(
        ('Accepted','Accepted'),
        ('Declined', 'Declined'),
        ('Pending', 'Pending')
    )
    jobapply_id=models.ForeignKey(job, on_delete=models.CASCADE)
    applicant=models.ForeignKey(jobseeker, on_delete=models.CASCADE)
    resume=models.FileField(upload_to="media")
    applydate=models.DateTimeField(auto_now_add=True, null=True)
    status=models.CharField(max_length=20, choices=status_choices)

class Contact(models.Model):
    subject = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.CharField(max_length=200)

class Subscriber(models.Model):
    email = models.EmailField()
    date_subscribed = models.DateTimeField(auto_now_add=True)
