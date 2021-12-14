from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from authentication.models import UserDetail

class TestView(View):
    def get(self, request, service=None):
        return render(request,'test.html')

class AuthenticationView(View):
    def get(self, request, service=None):
        if service=="logout":
            auth_logout(request)
            return redirect('authentication:index')

        return render(request,'index.html')

    def post(self, request, service=None):
        data={
            "message":""
        }
        try:
            if service=="register": 
                name=request.POST.get("name")
                username=request.POST.get("username")
                password=request.POST.get("password")
                confirm_password=request.POST.get("confirm_password")
                obj=None
                try:
                    obj = User.objects.get(username=username)
                except:
                    pass
                if obj:
                    data["message"]="User Already Exist"
                    raise ValueError("User Already Exist")

                if password!=confirm_password:
                    data["message"]="Password and Confirm Password not Matched"

                else:
                    User.objects.create(username=username, password=password)
                
                user=User.objects.get(username=username)
                UserDetail.objects.create(user=user, name=name)    
                auth_login(request,user)
                    
            elif service=="login":
                
                username=request.POST.get("username")
                password=request.POST.get("password")
                try:
                    user=User.objects.get(username=username,password=password)
                    auth_login(request,user)
                except:
                    data["message"]="Invalid Email or Password"
                    raise ValueError("Invalid Email or Password")

            return redirect("home:dashboard")

        except Exception as e:
            print(str(e))
            return redirect('index')