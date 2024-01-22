from .models import recruiter, jobseeker

def recruiter_info(request):
    recruiter_image = ''
    recruiter_company = ''

    if request.user.is_authenticated and request.user.usertype == 'recruiter':
        try:
            recruiter_data = recruiter.objects.get(recruiter_id=request.user)
            recruiter_image = recruiter_data.image.url
        except recruiter.DoesNotExist:
            pass

    return {
        'recruiter_image': recruiter_image,
        'recruiter_company': recruiter_company,
    }


def jobseeker_info(request):
    jobseeker_image = ''

    if request.user.is_authenticated and request.user.usertype == 'jobseeker':
        try:
            jobseeker_data = jobseeker.objects.get(emp_id=request.user)
            jobseeker_image = jobseeker_data.image.url
        except recruiter.DoesNotExist:
            pass

    return {
        'jobseeker_image': jobseeker_image,
    }
