from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Note, SecurityLog

def get_current_user(request):
    """Helper to get user from session."""
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
    return None

@csrf_exempt
def login_view(request):
    if get_current_user(request):
        return redirect('dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # # -------------------------------------------------------------------------
        # # FLAW 3: A03 - SQL Injection
        # # FLAW 2: A02 - Cryptographic Failures (Plaintext Password)
        # # FLAW 5: A07 - Identification and Authentication Failures (No Lockout)
        # # FLAW 4: A09 - Security Logging and Monitoring Failures (No Logging)
        # # -------------------------------------------------------------------------

        # >>> START OF INCORRECT CODE (Wrap this entire block in triple quotes when securing the app) >>>
        cursor = connection.cursor()
        query = f"SELECT id, username, password, is_admin, is_blocked, failed_login_attempts FROM notes_app_customuser WHERE username = '{username}'"
        cursor.execute(query)
        row = cursor.fetchone()

        if not row:
            error = "Invalid username or password."
        else:
            user_id, db_username, db_password, is_admin, is_blocked, failed_attempts = row
            password_matches = (db_password == password)

            if password_matches:
                request.session['user_id'] = user_id
                request.session['username'] = db_username
                request.session['is_admin'] = is_admin
                return redirect('dashboard')
            else:
                error = "Invalid username or password."
        # <<< END OF INCORRECT CODE <<<

        # # -------------------------------------------------------------------------
        # # REMEDIATION (A03, A02, A07, A09)
        # # Remove the triple quotes (""") below to activate this secure code block.
        # # -------------------------------------------------------------------------
        
        
        # >>> START OF CORRECT CODE >>>
        user = CustomUser.objects.filter(username=username).first()  # Prevents SQL Injection using ORM (A03)
        if not user:
            error = "Invalid username or password."
            SecurityLog.objects.create(
                message=f"Failed login attempt for non-existent username: '{username}'", 
                severity='WARNING'  # Logs failed login attempts for non-existent users (A09)
            )
        else:
            if user.is_blocked:
                error = "This account is blocked due to 10 failed login attempts. Contact an admin."  # Blocks access if account is locked (A07)
                return render(request, 'login.html', {'error': error})

            password_matches = check_password(password, user.password)  # Validates password against secure hash (A02)
            if password_matches:
                user.failed_login_attempts = 0  # Resets failed attempts counter on success (A07)
                user.save()

                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['is_admin'] = user.is_admin
                return redirect('dashboard')
            else:
                error = "Invalid username or password."
                user.failed_login_attempts += 1  # Increments failed attempts counter (A07)
                if user.failed_login_attempts >= 10:
                    user.is_blocked = True  # Locks account after 10 failed attempts (A07)
                user.save()

                SecurityLog.objects.create(
                    message=f"Failed login attempt for user: '{user.username}'", 
                    severity='WARNING'  # Logs failed login attempt (A09)
                )
                if user.failed_login_attempts >= 5:
                    SecurityLog.objects.create(
                        message=f"CRITICAL: User '{user.username}' has reached {user.failed_login_attempts} failed login attempts consecutively!", 
                        severity='CRITICAL'  # Critical log for suspected brute-force attempt (A09)
                    )
        # <<< END OF CORRECT CODE <<<

    return render(request, 'login.html', {'error': error})

@csrf_exempt
def register_view(request):
    if get_current_user(request):
        return redirect('dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            error = "Please fill in all fields."
        elif CustomUser.objects.filter(username=username).exists():
            error = "Username already exists."
        else:
            # # -------------------------------------------------------------------------
            # # FLAW 2: A02 - Cryptographic Failures (Plaintext Password Storage)
            # # -------------------------------------------------------------------------

            # >>> START OF INCORRECT CODE (Wrap this entire block in triple quotes when securing the app) >>>
            CustomUser.objects.create(username=username, password=password, is_admin=False)
            # <<< END OF INCORRECT CODE <<<

            # # -------------------------------------------------------------------------
            # # REMEDIATION (A02)
            # # Remove the triple quotes (""") below to activate this secure code block.
            # # -------------------------------------------------------------------------


            # >>> START OF CORRECT CODE >>>
            
            """ CustomUser.objects.create(
                username=username,
                password=make_password(password),  # Securely hashes password using PBKDF2 (A02)
                is_admin=False
            ) """
           
            # <<< END OF CORRECT CODE <<<            


            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

    return render(request, 'register.html', {'error': error})

def logout_view(request):
    request.session.flush()
    return redirect('login')

@csrf_exempt
def dashboard_view(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Note.objects.create(user=user, content=content)
            messages.success(request, "Note saved successfully!")
            return redirect('dashboard')

    user_notes = Note.objects.filter(user=user).order_by('-id')
    return render(request, 'dashboard.html', {
        'user': user,
        'notes': user_notes
    })

def admin_panel_view(request):
    # # -------------------------------------------------------------------------
    # # FLAW 1: A01 - Broken Access Control
    # # FLAW 4: A09 - Security Logging and Monitoring Failures (Bypassed Status Actions)
    # # -------------------------------------------------------------------------

    # >>> START OF INCORRECT CODE (Wrap this entire block in triple quotes when securing the app) >>>
    if 'user_id' not in request.session:
        return redirect('login')
    
    users = CustomUser.objects.all().order_by('username')
    notes = Note.objects.all().order_by('-id')
    logs = None
    # <<< END OF INCORRECT CODE <<<

    # # -------------------------------------------------------------------------
    # # REMEDIATION (A01, A09)
    # # Remove the triple quotes (""") below to activate this secure code block.
    # # -------------------------------------------------------------------------
    
    
    # >>> START OF CORRECT CODE >>>
    """ if 'user_id' not in request.session:
        return redirect('login')
    if not request.session.get('is_admin', False):
        return render(request, 'unauthorized.html', status=403)  # Restricts access to non-admins (A01)

    users = CustomUser.objects.all().order_by('username')
    notes = Note.objects.all().order_by('-id')

    action = request.GET.get('action')
    target_id = request.GET.get('user_id')
    if action and target_id:
        try:
            target_user = CustomUser.objects.get(id=target_id)
            if action == 'block':
                target_user.is_blocked = True
                target_user.failed_login_attempts = 10
                SecurityLog.objects.create(message=f"Admin blocked user '{target_user.username}'", severity='INFO')  # Logs admin blocking user (A09)
            elif action == 'unblock':
                target_user.is_blocked = False
                target_user.failed_login_attempts = 0
                SecurityLog.objects.create(message=f"Admin unblocked user '{target_user.username}'", severity='INFO')  # Logs admin unblocking user (A09)
            target_user.save()
            messages.success(request, f"User {target_user.username} {action}ed successfully.")
        except CustomUser.DoesNotExist:
            pass
        return redirect('admin_panel')

    logs = SecurityLog.objects.all().order_by('-created_at') """  # Loads security logs for admin monitoring (A09)
   
    # <<< END OF CORRECT CODE <<<

    return render(request, 'admin_panel.html', {
        'users': users,
        'notes': notes,
        'logs': logs
    })
