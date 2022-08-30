from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')
def login(request):
    if request.method== 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user= authenticate(username=username, password=password)
    return render(request,'index.html')

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # check password equality
        if password1 == password2:
            users = User.objects.all()
            for u in users:
                if u.username == username:
                    return render(request, 'register.html', context={
                        'error_message': "User already exists!"
                    })
            # user does not exist, create new
            new_user = User.objects.create_user(username, username, password1)
            new_user.is_staff = False
            new_user.is_active = False
            new_user.is_superuser = False
            new_user.save()
            # create activation link
            new_user_id = str(new_user.id)
            link = "http://127.0.0.1:8000/restaurant/activation/"+new_user_id+"/"
            message_text = "Click on the following link to complete your registration\n\n" + link
            # sending email
            send_mail('Restaurant - Profile Activation', message_text, 'testmail1836@gmail.com', [new_user.username],
                      fail_silently=False)
            # creating guest object
            new_guest = Guest.objects.create(user=new_user)
            new_user.save()
            print("Successful! Guest inserted: " + str(new_guest))

            # back on page
            return render(request, 'register.html', context={
                'info_message': "Account created successfully. Email with activation link was sent!"
            })
        else:
            return render(request, 'register.html', context={
                'error_message': "Password wasn't repeated correctly!"
            })
