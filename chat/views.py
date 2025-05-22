from django.shortcuts import render, redirect
from file.models import UserProfile
from .forms import LoginForm
from .models import ChatTable

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            try:
                user = UserProfile.objects.get(username=uname, password=pwd)
                request.session['user_id'] = user.id  # login via session
                return redirect('list_view')  
            except UserProfile.DoesNotExist:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_list_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    current_user = UserProfile.objects.get(id=user_id)
    users = UserProfile.objects.exclude(id=user_id)
    return render(request, 'user_list.html', {'users': users, 'current_user': current_user})

def chat_page(request, receiver_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    sender = UserProfile.objects.get(id=user_id)
    receiver = UserProfile.objects.get(id=receiver_id)

    chats = ChatTable.objects.filter(
        sender__in=[sender, receiver],
        receiver__in=[sender, receiver]
    ).order_by('timestamp')

    return render(request, 'chat.html', {
        'chats': chats,
        'sender': sender,
        'receiver': receiver
    })


    