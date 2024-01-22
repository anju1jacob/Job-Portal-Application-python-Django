from django.shortcuts import render, redirect,HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from jobportal import settings
from django.core.mail import send_mail
from .models import User,jobseeker, recruiter, company, company_gallery, job, apply, Contact, Subscriber
from datetime import date
from .filter import Jobfilter


# general views
def home(request):
    data=job.objects.all().order_by('-startdate')[:8]
    return render(request,'home.html', {'data':data})

def registration(request):
    return render(request,'registration.html')

def about(request):
    return render(request,'about.html')

def contacts(request):
    if request.method == 'POST':
        
        try:
            message = request.POST['message']
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            
            # Create a Contact instance and save it
            contact_instance = Contact.objects.create(
                message=message,
                name=name,
                email=email,
                subject=subject
            )
            
            # Sending email
            send_mail(subject, f"UserEmail :{email}\nUsername:{name}\n\n\n QUERY : {message}\n\n\nfaithfully\n{name}", email, [settings.EMAIL_HOST_USER], fail_silently=False)
            
            return render(request, 'contact.html', {'name': name})  
        except Exception as e:
           
            print(e)  
           
    return render(request, 'contact.html')  


def subscribe(request):
    if request.method == 'POST':
        print("Received POST request for subscription")
        email = request.POST.get('email')
        if email:
            subscriber = Subscriber(email=email)
            subscriber.save()
            return JsonResponse({'message': 'Thank you for subscribing!'})
        else:
            return JsonResponse({'error': 'Email is required'}, status=400)


def joblist(request):
    data=job.objects.all().order_by('-startdate')
    filter=Jobfilter(request.GET, queryset=job.objects.filter(is_available=True).order_by('-startdate'))
    return render(request,'joblist.html', {'filter':filter})

def loginpage(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request, username=email, password=password)
        if user is not None and user.is_superuser == 1:
            login(request,user)
            request.session['id']=user.id
            return redirect('admin_home')
        elif user is not None and user.is_staff==1:
           login(request, user)
           request.session['recruiter_id']=user.id
           return redirect('recruiter_home')
        elif user is not None and user.usertype=='jobseeker':
           login(request, user)
           request.session['emp_id']=user.id
           return redirect('jobseeker_home')
        else:
            messages.warning(request,'something went wrong, Please try again!')
            return render(request, 'loginpage.html')
    else:
        return render(request,'loginpage.html')
    
def forgetpwd(request):
    if request.method == 'POST':
        sub = request.POST.get('Email')
        subject = 'Job Flnder - password Reset'
        message = 'Please click the link to reset your password http://127.0.0.1:8000/passwordreset'
        recepient = str(sub)
        send_mail(subject,
                  message, settings.EMAIL_HOST_USER, [recepient], fail_silently=False)
        messages.success(request, 'Please check your Email to reset password')
        return render(request, 'forgetpwd.html', {'recepient': recepient})
    return render(request,'forgetpwd.html')


def passwordreset(request):
    return render(request, 'passwordreset.html')     
    
def reset(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['commail'] ).exists():
            member = User.objects.get(email=request.POST['commail'])
            return render(request, 'reset.html',{'member': member})
        else:
            context = {'msg': 'Invalid Username '}
            return render(request, 'passwordreset.html', context)
        
def update(request, id):
    if request.method == 'POST':
        current_password = request.POST.get('compassword')
        confirm_password = request.POST.get('comconpassword')
        
        if current_password and confirm_password and current_password == confirm_password:
            try:
                member = User.objects.get(id=id)
                member.set_password(confirm_password)
                member.save()
                messages.success(request,'Password updated successfully. Please Login..')
                return redirect('loginpage') 
            except User.DoesNotExist:
                pass  
        return render(request, 'passwordreset.html')  
    else:
        return render(request, 'passwordreset.html') 
    
        
def logout_user(request):
    logout(request)
    messages.info(request,'your session has ended, Please Login to continue..')
    return redirect('loginpage')


# Jobseeker's module views

def jobseeker_register(request):
    if request.method =='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        mail=request.POST['mail']
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        phone=request.POST['phone']
        pics=request.FILES['pic']

        add=User.objects.create_user(first_name=fname, last_name=lname, email=mail, username=uname, password=pwd, usertype='jobseeker')
        add.save()
        s=jobseeker.objects.create(emp_id=add, phone=phone, image=pics)
        s.save()
        messages.info(request,'Your account has been created, Please login')
        return redirect('loginpage')
    else:      
        return render(request,'jobseeker_register.html')
    
def jobseeker_home(request):
    emp_id = request.session.get('emp_id', None)
    if emp_id is not None: 
        data=jobseeker.objects.get(emp_id=emp_id) 
        return render(request,'jobseeker_home.html',{'data':data})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    
def jobseeker_changepwd(request):
    emp_id = request.session.get('emp_id', None)
    if emp_id is not None:
        error1=""
        error2=""
        if request.method =='POST':
            currentpwd=request.POST['currentpwd']
            newpwd=request.POST['newpwd']
            u=User.objects.get(id=emp_id)
            if u.check_password(currentpwd):
                u.set_password(newpwd)
                u.save()
                error1='no'
                return render(request,'jobseeker_changepwd.html',{'error1':error1})
            else:
                error2='not'
                return render(request,'jobseeker_changepwd.html',{'error2':error2})
        else:
                return render(request,'jobseeker_changepwd.html')

    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def jobseeker_profile(request):
    emp_id = request.session.get('emp_id', None)
    if emp_id is not None:
        data=jobseeker.objects.get(emp_id=emp_id)
        if request.method =='POST':
            fname=request.POST['fname']
            lname=request.POST['lname']
            mail=request.POST['mail']
            uname=request.POST['uname']
            phone=request.POST['phone']

            if 'pic' in request.FILES:
                pics = request.FILES['pic']
                data.image = pics

            y=data.emp_id
            y.first_name=fname
            y.last_name=lname
            y.email=mail
            y.username=uname
            data.phone=phone
            data.save()
            y.save()

            error1='no'
            return render(request,'jobseeker_profile.html',{'error1':error1})
        else:
            return render(request,'jobseeker_profile.html', {'data':data})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    
    
def jobseeker_view_joblist(request):
    emp_id = request.session.get('emp_id', None)
    if emp_id is not None:
        data=job.objects.all().order_by('-startdate')
        filter=Jobfilter(request.GET, queryset=job.objects.filter(is_available=True).order_by('-startdate'))
        data2=jobseeker.objects.get(emp_id=emp_id)
        data1=apply.objects.filter(applicant=data2)
        li=[]
        for i in data1:
            li.append(i.jobapply_id.id)
        return render(request,'jobseeker_view_joblist.html',{'data':data, 'li':li, 'filter':filter})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    
def jobseeker_jobdetails(request, id):
    emp_id = request.session.get('emp_id', None)
    if emp_id is not None:
        job_data = get_object_or_404(job, id=id)
        ideal_candidate_list = job_data.ideal_candidate.split(',') 
        experience=job_data.experience.split(',')
        return render(request, 'jobseeker_jobdetail_view.html', {'job_data': job_data, 'ideal_candidate_list': ideal_candidate_list, 'experience':experience})
    else:
        messages.warning(request, 'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def jobseeker_applyjob(request, id):
    emp_id = request.session.get('emp_id', None)
    error1 = None  

    if emp_id is not None:
        seekers = jobseeker.objects.get(emp_id=emp_id)
        applyjob = job.objects.get(id=id)
        date1 = date.today()

        if applyjob.enddate < date1:
            error1 = 'close'
        else:
            if request.method == 'POST':
                cv = request.FILES['resume']
                add = apply.objects.create(applicant=seekers, jobapply_id=applyjob, resume=cv, applydate=date.today(), status='pending')
                add.save()
                error='no'
                return render(request, 'jobseeker_applyjob.html', {'error': error})

        return render(request, 'jobseeker_applyjob.html', {'error1': error1})
    else:
        messages.warning(request, 'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def jobseeker_view_company(request):
    emp_id = request.session.get('emp_id', None)
    if emp_id is not None:
        data=company.objects.all()
        return render(request,'jobseeker_view_company.html', {'data':data})
    else:
        messages.warning(request, 'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def jobseeker_view_companydetails(request,id):
    emp_id = request.session.get('emp_id', None)
    if emp_id is not None:
        data=company.objects.get(id=id)
        comp_id=data.id
        view=company_gallery.objects.filter(company_imgid=comp_id)
        return render(request,'jobseeker_view_companydetails.html', {'data':data, 'view':view})
    else:
        messages.warning(request, 'Invalid session data. Please log in again.')
        return redirect('loginpage')


def jobseeker_view_myjoblist(request):
    emp_id = request.session.get('emp_id', None)
    if emp_id is not None:
        seeker=jobseeker.objects.get(emp_id=emp_id)
        appliedjob = apply.objects.all().filter(applicant=seeker).order_by('-applydate')
        return render(request,'jobseeker_view_myjoblist.html',{'appliedjob':appliedjob})
    else:
        messages.warning(request, 'Invalid session data. Please log in again.')
        return redirect('loginpage')

    

# Recruiter module views

def recruiter_register(request):
    if request.method =='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        mail=request.POST['mail']
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        phone=request.POST['phone']
        pics=request.FILES['pic']
        compname=request.POST['cmpname']
        pos=request.POST['position']

        add=User.objects.create_user(first_name=fname, last_name=lname, email=mail, username=uname, password=pwd, usertype='recruiter', is_staff=False)
        add.save()
        s=recruiter.objects.create(recruiter_id=add, phone=phone, image=pics, companyname=compname, position=pos, status='pending')
        s.save()
        messages.warning(request,'Your Account is not approved now. Our Team is checking your profile, Soon your account will be confirmed !!!')
        return redirect('loginpage')
    else:      
        return render(request,'recruiter_register.html')
    
    
def recruiter_home(request):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        data=recruiter.objects.get(recruiter_id=recruiter_id) 
        return render(request,'recruiter_home.html', {'data':data})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    
    
def recruiter_changepwd(request):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        error1=""
        error2=""
        if request.method =='POST':
            currentpwd=request.POST['currentpwd']
            newpwd=request.POST['newpwd']
            u=User.objects.get(id=recruiter_id)
            if u.check_password(currentpwd):
                u.set_password(newpwd)
                u.save()
                error1='no'
                return render(request,'recruiter_changepwd.html',{'error1':error1})
            else:
                error2='not'
                return render(request,'recruiter_changepwd.html',{'error2':error2})
        else:
                return render(request,'recruiter_changepwd.html')
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    
    
def recruiter_profile(request):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        data=recruiter.objects.get(recruiter_id=recruiter_id)
        if request.method =='POST':
            fname=request.POST['fname']
            lname=request.POST['lname']
            mail=request.POST['mail']
            uname=request.POST['uname']
            compname=request.POST['compname']
            position=request.POST['position']
            phone=request.POST['phone']

            if 'pic' in request.FILES:
                pics = request.FILES['pic']
                data.image = pics

            y=data.recruiter_id
            y.first_name=fname
            y.last_name=lname
            y.email=mail
            y.username=uname
            data.companyname=compname
            data.position=position
            data.phone=phone
            data.save()
            y.save()

            error1='no'
            return render(request,'recruiter_profile.html',{'error1':error1})
        else:
            return render(request,'recruiter_profile.html', {'data':data})            
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def recruiter_addcompany(request):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        if request.method =='POST':
            comptype=request.POST['comptype']
            pics=request.FILES['pic']
            mail=request.POST['mail']
            about=request.POST['about']
            city=request.POST['city']
            state=request.POST['state']
            date=request.POST['date']
            phone=request.POST['phone']
            
            logged_in_user = request.user
            recruiter_obj = recruiter.objects.get(recruiter_id=logged_in_user)
            s=company.objects.create(company_id=recruiter_obj, company_type=comptype, logo=pics, company_email=mail,
                                     about=about, city=city, state=state, est_date=date, company_phn=phone)
            s.save()
            success_message = "yes"
            return render(request,'recruiter_addcompany.html', {'success_message':success_message})
        else:
            return render(request,'recruiter_addcompany.html')
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    
def recruiter_company(request):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        data1=recruiter.objects.get(recruiter_id=recruiter_id)
        data_id=data1.id
        try:
            data=company.objects.get(company_id=data_id) 
        except company.DoesNotExist:
            error='yes'
            return render(request, 'recruiter_company.html', {'error': error})
        if request.method =='POST':
            companyname=request.POST['companyname']
            comptype=request.POST['comptype']
            mail=request.POST['mail']
            about=request.POST['about']
            city=request.POST['city']
            state=request.POST['state']
            phone=request.POST['phone']
            date=request.POST['date']

            if 'pic' in request.FILES:
                pics = request.FILES['pic']
                data.logo = pics
            else:
                pass

            if date:
                data.est_date=date
                data.save()
            else:
                pass

            y=data.company_id
            y.companyname=companyname
            
            data.company_type=comptype
            data.company_email=mail
            data.about=about
            data.city=city
            data.state=state
            data.company_phn=phone
            data.save()
            y.save()

            error1='no'
            return render(request,'recruiter_company.html',{'error1':error1}) 
        else:  
            return render(request,'recruiter_company.html', {'data':data})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    
def recruiter_company_gallery(request):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None:
        company_images=''
        current_recruiter=recruiter.objects.get(recruiter_id=recruiter_id)
        current_recruiter_id=current_recruiter.id
        try:
            current_company=company.objects.get(company_id=current_recruiter_id) 
            current_company_id=current_company.id
        except company.DoesNotExist:
            error='yes'
            return render(request, 'recruiter_company_gallery.html', {'error': error})

        if request.method == 'POST':
            uploaded_images = request.FILES.getlist('pic')
            for image in uploaded_images:
                new_image = company_gallery(
                    recruiter_imgid_id=current_recruiter_id,
                    company_imgid_id=current_company_id,
                    companyimage=image
                )
                new_image.save()

        company_images = company_gallery.objects.filter(company_imgid=current_company_id)
        return render(request, 'recruiter_company_gallery.html', {'company_images': company_images})
        
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')


def recruiter_postjob(request):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None:
        current_recruiter=recruiter.objects.get(recruiter_id=recruiter_id)
        current_recruiter_id=current_recruiter.id
        job_types = job.JOB_TYPES
        success_message=''
        try:
            current_company=company.objects.get(company_id=current_recruiter_id) 
            current_company_id=current_company.id
            
        except company.DoesNotExist:
            error='yes'
            return render(request, 'recruiter_postjob.html', {'error': error})
        
        if request.method =='POST':
            title=request.POST['title']
            enddate=request.POST['enddate']
            description=request.POST['description']
            requirements=request.POST['requirements']
            experience=request.POST['experience']
            job_type=request.POST['job_type']
            salary=request.POST['salary']
            location=request.POST['location']
            vaccancy=request.POST['vaccancy']
            
            add=job.objects.create(job_id=current_recruiter, job_compid=current_company, title=title, enddate=enddate, salary=salary,
                                   ideal_candidate=requirements ,experience=experience, description=description, job_type=job_type,
                                   location=location, vaccancy=vaccancy)
            add.save()
            success_message = "yes"
        return render(request, 'recruiter_postjob.html',{'job_types':job_types, 'success_message':success_message})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def recruiter_managejobs(request):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        userid=recruiter.objects.get(recruiter_id=recruiter_id)
        user=userid.id
        jobs=job.objects.filter(job_id=user).order_by('-startdate')
        return render(request,'recruiter_managejobs.html',{'jobs':jobs})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def recruiter_update_jobpost(request,id):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None:
        jobs=job.objects.get(id=id)
        job_types = job.JOB_TYPES

        if request.method =='POST':
            title=request.POST['title']
            enddate=request.POST['enddate']
            description=request.POST['description']
            requirements=request.POST['requirements']
            experience=request.POST['experience']
            job_type=request.POST['job_type']
            salary=request.POST['salary']
            location=request.POST['location']
            vaccancy=request.POST['vaccancy']

            jobs.title=title
            jobs.salary=salary
            jobs.description=description
            jobs.ideal_candidate=requirements
            jobs.experience=experience
            jobs.location=location
            jobs.vaccancy=vaccancy
            jobs.job_type=job_type
           
            jobs.save()

            if enddate:
                jobs.enddate=enddate
                jobs.save()
            else:
                pass

            if 'is_available' in request.POST:
                is_available_value = request.POST.get('is_available')
                if is_available_value == 'on':  # Checkbox is checked
                    jobs.is_available = True
                else:
                    jobs.is_available = False
            else:
               
                pass

            jobs.save()

            success_message = "yes"
            return render(request,'recruiter_update_jobpost.html', {'success_message':success_message})

        return render(request,'recruiter_update_jobpost.html',{'jobs':jobs, 'job_types':job_types})
    else:
            messages.warning(request,'Invalid session data. Please log in again.')
            return redirect('loginpage')
    

def recruiter_view_applications(request):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        userid=recruiter.objects.get(recruiter_id=recruiter_id)
        user=userid.id
        jobs=job.objects.filter(job_id=user)
        return render(request,'recruiter_view_applications.html',{'jobs':jobs})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def recruiter_view_listof_application(request,id):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        jobs=job.objects.get(id=id)
        applicants=jobs.apply_set.all().order_by('-applydate')

        return render(request,'recruiter_view_listof_application.html',{'jobs':jobs, 'applicants':applicants})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def recruiter_accept_applicant(request,id):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        job_application = apply.objects.get(id=id)
        job_application.status = 'Accepted'
        job_application.save()
        # Get the applicant's email
        applicant_email = job_application.applicant.emp_id.email
                
                # Get the email of the logged-in recruiter
        recruiter_email = request.user.email
                
                # Sending the email
        subject = 'Application Accepted'
        message = 'Your application has been accepted. Congratulations!'
        send_mail(subject, message, recruiter_email, [applicant_email], fail_silently=False)
                
        return redirect('recruiter_view_listof_application', id=job_application.jobapply_id.id)

    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def recruiter_reject_applicant(request,id):
    recruiter_id = request.session.get('recruiter_id', None)
    if recruiter_id is not None: 
        job_application = apply.objects.get(id=id)
        job_application.status = 'Declined'
        job_application.save()
        # Get the applicant's email
        applicant_email = job_application.applicant.emp_id.email
                
                # Get the email of the logged-in recruiter
        recruiter_email = request.user.email
                
                # Sending the email
        subject = 'Application Declined'
        message = 'Your application has been Declined. Better luck next time!'
        send_mail(subject, message, recruiter_email, [applicant_email], fail_silently=False)
                
        return redirect('recruiter_view_listof_application', id=job_application.jobapply_id.id)

    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')


#admin module views

def admin_home(request):
    id=request.session.get('id', None)
    if id is not None:
        #for cards
        total=jobseeker.objects.all().count()
        totalcount=recruiter.objects.all().count()
        jobs=job.objects.all().count()
        acceptedcount=recruiter.objects.all().filter(status='accepted').count()
        pendingcount=recruiter.objects.all().filter(status='pending').count()
        rejectcount=recruiter.objects.all().filter(status='rejected').count()

           #for table in admin dashboard
        provider=recruiter.objects.all().order_by('-id')
        candidate=jobseeker.objects.all().order_by('-id')
        return render(request,'admin_home.html',{'acceptedcount':acceptedcount, 'pendingcount':pendingcount, 
                                                 'totalcount':totalcount, 'rejectcount':rejectcount, 'jobs':jobs,
                                                 'total':total, 'provider':provider, 'candidate':candidate})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def admin_add_recruiter(request):
    id=request.session.get('id', None)
    if id is not None:
        if request.method =='POST':
            fname=request.POST['fname']
            lname=request.POST['lname']
            mail=request.POST['mail']
            uname=request.POST['uname']
            pwd=request.POST['pwd']
            phone=request.POST['phone']
            pics=request.FILES['pic']
            compname=request.POST['cmpname']
            pos=request.POST['position']

            add=User.objects.create_user(first_name=fname, last_name=lname, email=mail, username=uname, password=pwd, usertype='recruiter', is_staff=True)
            add.save()
            s=recruiter.objects.create(recruiter_id=add, phone=phone, image=pics, companyname=compname, position=pos, status='accepted')
            s.save()
            success_message = "yes"
            return render(request,'admin_add_recruiter.html',{'success_message':success_message})
        else:
            return render(request,'admin_add_recruiter.html')
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def admin_changepwd(request):
    id=request.session.get('id', None)
    if id is not None:
        error1=""
        error2=""
        if request.method =='POST':
            currentpwd=request.POST['currentpwd']
            newpwd=request.POST['newpwd']
            u=User.objects.get(id=id)
            if u.check_password(currentpwd):
                u.set_password(newpwd)
                u.save()
                error1='no'
                return render(request,'admin_changepwd.html',{'error1':error1})
            else:
                error2='not'
                return render(request,'admin_changepwd.html',{'error2':error2})
        else:
                return render(request,'admin_changepwd.html')
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def admin_view_pendingrecruiter(request):
    id=request.session.get('id', None)
    if id is not None:
        data=recruiter.objects.all().filter(status='pending').order_by('-id')
        return render(request,'admin_view_pendingrecruiter.html', {'data':data})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def admin_delete_pendingrecruiter(request,id):
    data=recruiter.objects.get(id=id)
    user_id =data.recruiter_id.id
    user_mail=data.recruiter_id.email
    data.delete()
    User.objects.filter(id=user_id).delete()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account Deletion Notification'
        message = 'Your recruiter profile has been deleted.If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_pendingrecruiter')
    

def admin_approve_pendingrecruiter(request,id):
    confirm=recruiter.objects.select_related('recruiter_id').get(id=id)
    confirm.recruiter_id.is_staff=True
    user_mail=confirm.recruiter_id.email
    confirm.recruiter_id.save()
    confirm.status='accepted'
    confirm.save()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account confirmation Notification'
        message = 'Your recruiter profile has been confirmed.Now you can login to your account, If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_pendingrecruiter')
    

def admin_reject_pendingrecruiter(request,id):
    confirm=recruiter.objects.select_related('recruiter_id').get(id=id)
    confirm.recruiter_id.is_staff=False
    user_mail=confirm.recruiter_id.email
    confirm.recruiter_id.save()
    confirm.status='rejected'
    confirm.save()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account Rejection Notification'
        message = 'Your recruiter profile has been rejected. If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_pendingrecruiter')
      
    
def admin_view_acceptedrecruiter(request):
    id=request.session.get('id', None)
    if id is not None:
        data=recruiter.objects.all().filter(status='accepted').order_by('-id')
        return render(request,'admin_view_acceptedrecruiter.html', {'data':data})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def admin_delete_acceptedrecruiter(request,id):
    data=recruiter.objects.get(id=id)
    user_id =data.recruiter_id.id
    user_mail=data.recruiter_id.email
    data.delete()
    User.objects.filter(id=user_id).delete()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account Deletion Notification'
        message = 'Your recruiter profile has been deleted.If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_acceptedrecruiter')
    

def admin_reject_acceptedrecruiter(request,id):
    confirm=recruiter.objects.select_related('recruiter_id').get(id=id)
    confirm.recruiter_id.is_staff=False
    user_mail=confirm.recruiter_id.email
    confirm.recruiter_id.save()
    confirm.status='rejected'
    confirm.save()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account Rejection Notification'
        message = 'Your recruiter profile has been rejected. If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_acceptedrecruiter')
    

def admin_pending_acceptedrecruiter(request,id):
    confirm=recruiter.objects.select_related('recruiter_id').get(id=id)
    confirm.recruiter_id.is_staff=False
    user_mail=confirm.recruiter_id.email
    confirm.recruiter_id.save()
    confirm.status='pending'
    confirm.save()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account Pending Notification'
        message = 'Your recruiter profile has been pending. If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_acceptedrecruiter')


def admin_view_rejectedrecruiter(request):
    id=request.session.get('id', None)
    if id is not None:
        data=recruiter.objects.all().filter(status='rejected').order_by('-id')
        return render(request,'admin_view_rejectedrecruiter.html', {'data':data})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def admin_delete_rejectedrecruiter(request,id):
    data=recruiter.objects.get(id=id)
    user_id =data.recruiter_id.id
    user_mail=data.recruiter_id.email
    data.delete()
    User.objects.filter(id=user_id).delete()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account Deletion Notification'
        message = 'Your recruiter profile has been deleted.If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_rejectedrecruiter')
    

def admin_approve_rejectedrecruiter(request,id):
    confirm=recruiter.objects.select_related('recruiter_id').get(id=id)
    confirm.recruiter_id.is_staff=True
    user_mail=confirm.recruiter_id.email
    confirm.recruiter_id.save()
    confirm.status='accepted'
    confirm.save()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account confirmation Notification'
        message = 'Your recruiter profile has been confirmed.Now you can login to your account, If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_rejectedrecruiter')
    

def admin_pending_rejectedrecruiter(request,id):
    confirm=recruiter.objects.select_related('recruiter_id').get(id=id)
    confirm.recruiter_id.is_staff=False
    user_mail=confirm.recruiter_id.email
    confirm.recruiter_id.save()
    confirm.status='pending'
    confirm.save()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account Pending Notification'
        message = 'Your recruiter profile has been pending. If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_rejectedrecruiter')
    

def admin_view_applicants(request):
    id=request.session.get('id', None)
    if id is not None:
        data=jobseeker.objects.all().order_by('-id')
        return render(request,'admin_view_applicants.html', {'data':data})
    else:
        messages.warning(request,'Invalid session data. Please log in again.')
        return redirect('loginpage')
    

def admin_delete_applicant(request,id):
    data=jobseeker.objects.get(id=id)
    user_id =data.emp_id.id
    user_mail=data.emp_id.email
    data.delete()
    User.objects.filter(id=user_id).delete()
    user_email = user_mail
    if user_email:
        subject = ' Job Flnder - Account Deletion Notification'
        message = 'Your jobseeker profile has been deleted.If you have any further question please contact us. ph:9879879879'
        to_email = user_email
        send_mail(subject, message, settings.EMAIL_HOST_USER,[to_email] )
        return redirect('admin_view_applicants')
    

