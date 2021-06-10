from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Post, Comment
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email_address = request.POST['email_address'],
            password = hashed_pw
        )
        request.session['user_id'] = user.id
        return redirect('/wall')

def login(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_list = User.objects.filter(email_address = request.POST['login_email'])
        if len(user_list) == 0:
            messages.error(request, 'A user with this email does not exists.')
            return redirect('/')
        else:
            user = user_list[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/wall')
            else:
                messages.error(request, 'Incorrect password or email.')
                return redirect('/')

def wall(request):
    print('*'*100)
    print('in the wall...')
    if 'user' not in request.session: #Make sure user is kicked back to index if not in session
        return redirect('/')
    context = {
        'fname' : request.session['first_name'],
        'messages' : Message.objects.all(),
        'comments' : Comment.objects.all(),
    }
    return render(request, 'wall.html', context)

def post_message(request):
    print('*'*100)
    print('creating message...')
    if request.method == 'POST':
        new_message = Message.objects.create(
            message_text = request.POST['msg'],
            user = User.objects.get(id = request.session['user'])
        )
        new_message.save()
    return redirect('/wall')

def post_comment(request, msg_id):
    print('*'*100)
    print('posting comment...')
    if request.method == 'POST':
        new_comment = Comment.objects.create(
            comment_text = request.POST['cmnt'],
            user = User.objects.get(id = request.session['user']),
            message = Message.objects.get(id = msg_id)
        )
        new_comment.save()
    return redirect('/wall')

def destroy(request):
    request.session.flush()
    return redirect('/')
