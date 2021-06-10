from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
from datetime import datetime
import bcrypt
import re


EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must at least contain two characters.'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must at least contain two characters.'
        if len(post_data['email_address']) < 1:
            errors['email_address'] = 'Please enter your full email address.'
        if not EMAIL_REGEX.match(post_data['email_address']):
            errors['email_valid'] = 'Please enter a valid email address.'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least eight characters long.'
        if len(post_data['password']) >= 8:
            if post_data['password'] != post_data['password_confirm']:
                    errors['password_no_match'] = 'Passwords do not match.'
        return errors

    def user_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['login_email']) < 1:
            errors['login_email'] = 'Please enter your full email address.'
        if not EMAIL_REGEX.match(post_data['login_email']):
            errors['login_email_valid'] = 'Please enter a valid email address.'
        if len(post_data['login_password']) < 1:
            errors['login_password'] = 'Please enter your password.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email_address = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    content = models.TextField()
    posted_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
