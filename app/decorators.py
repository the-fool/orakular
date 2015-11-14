from functools import wraps
from flask.ext.login import current_user
from flask import abort

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if role != current_user.role:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def student_only(f):
    return role_required('student')(f)
def staff_only(f):
    return role_required('staff')(f)
def faculty_only(f):
    return role_required('faculty')(f)
def non_student_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role.lower() == 'student':
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
