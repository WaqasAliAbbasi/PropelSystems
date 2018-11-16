from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from home.models import User

def user_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login', role=User.ADMIN):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == role,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def clinic_manager_required(*args):
    return user_required(*args, role=User.CLINIC_MANAGER)

def dispatcher_required(*args):
    return user_required(*args, role=User.DISPATCHER)

def admin_required(*args):
    return user_required(*args, role=User.ADMIN)

def warehouse_personnel_required(*args):
    return user_required(*args, role=User.WAREHOUSE_PERSONNEL)
