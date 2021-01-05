from django.shortcuts import render 
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.shortcuts import redirect
from django.utils.encoding import force_bytes , force_text , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from.utils import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry username is in use, chose another one'},status=409)
        return JsonResponse({'username_valid':True})      

class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'sorry email is in use, chose another one'},status=409)
        return JsonResponse({'email_valid':True})      


class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')  


    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            "fieldvalues" :request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'password Too sohrt')
                    return render(request,'authentication/register.html',context)  

                user = User.objects.create_user(email=email,username=username)
                user.set_password(password)
                user.is_active = False
                user.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(user)})
                activate_url = 'http//'+domain+link
                email_subject = 'Activate your account'

                email_body = 'HI '+user.username+ ' Please user this link to verify your account\n'+activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@m7moud.com',
                    [email],
                ) 
                EmailThread(email).start()
                messages.success(request,'Account successfully created check your mail to verify it')
                return render(request,'authentication/login.html')  

        return render(request,'authentication/register.html')  



    
class VarificationView(View):
    def get (self ,request ,uidb64 , token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user,token):
                return redirect ('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request,'Account activated successfully')
            return redirect('login')

        except Exception as ex :
            pass
        
        return redirect ('login')



    
class LoginView(View):
    def get (self ,request):
        return render(request,'authentication/login.html')

    def post(self,request):
        username=request.POST["username"]
        password=request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username , password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'Welcome '+user.username+' you are now logged in')
                    return redirect('/')
                else:
                    messages.info(request,'Account is not active ,please check your email')
                    return render(request,'authentication/login.html')
                    
            else:
                messages.error(request,'Invalid credntials,try again')
                return render(request,'authentication/login.html')
                

        messages.error(request,'Please fill all fields')
        return render(request,'authentication/login.html')


class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You have been logged out')
        return redirect('login')





class RequestPasswordRestEmail(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')



    def post(self,request):
        email = request.POST['email']


        context = {
            'values':email
        }

        if not validate_email(email):
            messages.error(request,'please entar vaild email')
            return render(request,'authentication/reset-password.html',context)

        current_site = get_current_site(request)
        user = User.objects.filter(email = email)
        if user.exists():
            
            email_contents = {
            'user': user[0],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password', kwargs={'uidb64':email_contents['uid'],'token':email_contents['token']})
            email_subject = 'Password reset instructions'

            reset_url = 'http//'+current_site.domain+link


            email = EmailMessage(
                email_subject,
                'HI there please click the link below to reset your password\n'+reset_url,
                'noreply@m7moud.com',
                [email],
            ) 
            EmailThread(email).start()

            messages.success(request,'we have sent you email to reset your password')

        if not user.exists():
            messages.error(request,'please registerd Email vaild email')

        
        return render(request,'authentication/reset-password.html')

class CompleatPasswordReset(View):
    def get(self,request,uidb64,token):
        context  ={
            'uidb64':uidb64,
            'token':token
        }

        
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):

                messages.info(request,'Password link is not valid request a new one')
                return render(request,'authentication/reset-password.html')
        except Exception as identifier:
           pass


    def post(self,request ,uidb64,token):
        context  ={
            'uidb64':uidb64,
            'token':token
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request,'Passwords is not match')
            return render(request,'authentication/set-new-password.html',context)
        if len(password)<6:
            messages.error(request,'Passwords is too short')
            return render(request,'authentication/set-new-password.html',context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,'Password rest successfully you can login with your new password')
            return redirect('login')
        except Exception as identifier:
            messages.info(request,'somthing went wrong , try again')

            return render(request,'authentication/set-new-password.html',context)
