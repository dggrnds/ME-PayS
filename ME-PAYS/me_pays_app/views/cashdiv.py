from me_pays_app.models.users import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django_cryptography.fields import *
from me_pays_app.models.balance import *
import hashlib

def user_has_cashier_group(user):
    return user.groups.filter(name='cashier').exists()



@user_passes_test(user_has_cashier_group)
@require_GET
def validate_SID(request):
    student_id = request.GET.get('school_id')
    
    if EndUser.objects.filter(school_id=student_id, user__is_active=1, rfid_code__isnull=True).exists():
        # Student ID is active and doesn't have an associated RFID
        return JsonResponse({'exists': 2})
    elif EndUser.objects.filter(school_id=student_id, user__is_active=1).exists():
        # Student ID already has an RFID associated and is active
        return JsonResponse({'exists': 3})
    elif EndUser.objects.filter(school_id=student_id, user__is_active=0).exists():
        # Student ID is inactive
        return JsonResponse({'exists': 1})
    else:
    # Student ID does not exist in the database
        return JsonResponse({'exists': 0})
    
@user_passes_test(user_has_cashier_group)
@require_GET
def load_validate_SID(request):
    student_id = request.GET.get('school_id')
    
    if EndUser.objects.filter(school_id=student_id, user__is_active=1, rfid_code__isnull=True).exists():
        # Student ID is active and doesn't have an associated RFID
        return JsonResponse({'exists': 2})
    elif EndUser.objects.filter(school_id=student_id, user__is_active=1).exists():
        # Student ID has an RFID associated
        return JsonResponse({'exists': 1})
    else:
    # Student ID does not exist in the database
        return JsonResponse({'exists': 3})

@user_passes_test(user_has_cashier_group)
@require_POST
def register_rfid_code(request):
    school_id = request.POST.get('school_id')
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    try:
        end_user = EndUser.objects.get(school_id=school_id)
        end_user.rfid_code = rfid
        end_user.save()

        return JsonResponse({'success': True, 'message': 'Registration Successful'})
    except EndUser.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'EndUser not found; Call the Administrator Immediately'})
    
 









@user_passes_test(user_has_cashier_group)
@require_GET
def validate_rfid(request):
    rfid = request.GET.get('rfid')
    hashed_rfid = hashlib.sha256(rfid.encode()).hexdigest()
    end_user = EndUser.objects.filter(rfid_code=hashed_rfid, user__is_active=1).first()
    
    if end_user is not None:
        # RFID instance already exists
        return JsonResponse({'exists': 1})
    else:
        # RFID code does not exist in the database
        return JsonResponse({'exists': 0})
    


@user_passes_test(user_has_cashier_group)
@require_POST
def load_validate_rfid(request):
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    if EndUser.objects.filter(rfid_code=rfid, user__is_active=1).exists():
        # RFID instance already exists
        return JsonResponse({'exists': 0})
    else:
        # RFID code does not exist in the database
        return JsonResponse({'exists': 1})
    
@user_passes_test(user_has_cashier_group)
@require_GET
def  load_rfid_creds(request):
    rfid = request.GET.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    user=EndUser.objects.filter(rfid_code=rfid).first()
    fullname = user.first_name+" "+user.last_name
    response = {
        'fullname': fullname,
        'personID': user.school_id
    }
    return JsonResponse(response)


@user_passes_test(user_has_cashier_group)
@require_GET
def load_cred_amount(request):
    rfid = request.GET.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    amount = request.GET.get('amount')
    user=EndUser.objects.filter(rfid_code=rfid).first()
    cashier = Cashier.objects.get(user=request.user)
    if user is not None:
        # Convert the amount to an integer if needed
        amount = int(amount)
        totalamount = amount*1.05
        # Add the amount to the current credit_balance
        user.credit_balance += totalamount
        # Save the updated user object
        user.save()
        # Save to Balance Logs
        log = Balance_Logs.objects.create(
            account_Owner = user,
            cashier_sender = cashier,
            amount = amount,
            desc = "Cash In",
        )  
        log.save()

        return JsonResponse({'status': 'success', 'message': 'Payment Successful, Please Check Your Load Balance'})
    else:
        return JsonResponse({'status': 'error', 'message': 'User not found, Contact Admin Immediately'})



       

