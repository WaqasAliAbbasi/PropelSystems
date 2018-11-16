from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from home.models import User

def user_required(role, function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
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

def clinic_manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    return user_required(role=User.CLINIC_MANAGER, function=function, redirect_field_name=redirect_field_name, login_url=login_url)

def dispatcher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    return user_required(role=User.DISPATCHER, function=function, redirect_field_name=redirect_field_name, login_url=login_url)

def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    return user_required(role=User.ADMIN, function=function, redirect_field_name=redirect_field_name, login_url=login_url)

def warehouse_personnel_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    return user_required(role=User.WAREHOUSE_PERSONNEL, function=function, redirect_field_name=redirect_field_name, login_url=login_url)
