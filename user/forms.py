from fileinput import FileInput
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', 
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(label='密  码', 
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名', 
                               max_length=20,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'取个名吧'}))
    last_name = forms.CharField(label='姓', required=False, 
                               max_length=20,
                               min_length=1,
                               widget=forms.TextInput(attrs={'class':'form-control',  'placeholder':'您老贵姓？'}))
    
    first_name = forms.CharField(label='名', required=False,
                               max_length=20,
                               min_length=1,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请教大名？'}))
    
    email = forms.EmailField(label='邮箱', required=False,
                             widget=forms.EmailInput(attrs={'class':'form-control',  'placeholder':'如何联系？'}))
    
    password = forms.CharField(label='密码', 
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'输入密码'}))
    password_again = forms.CharField(label='确认密码', 
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'没输错吧？再来一遍'}))

    avatar = forms.FileField(label='头像', required=False,
                                widget=forms.FileInput(attrs={'class':'form-control', 'placeholder':'展示一下您的绝世美颜呗'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('跟别人重名了！')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email!='' and User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱登记过了，是不是忘了您注册过了？')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('果然密码输错了！')
        return password_again

class ChangeNameForm(forms.Form):
    last_name_new = forms.CharField(
        label='姓', 
        max_length=20,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的姓'}
        )
    )
    first_name_new = forms.CharField(
        label='名', 
        max_length=20,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的名'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'请输入正确的邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        return email

class ChangeAvatarForm(forms.Form):
    avatar = forms.FileField(label='头像', required=False,
            widget=forms.FileInput(attrs={'class':'form-control', 'placeholder':'换一张更美的照片'})
        )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeAvatarForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'输入旧密码'}
        )
    )
    new_password = forms.CharField(
        label='新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'输入新密码'}
        )
    )
    new_password_again = forms.CharField(
        label='再输一次', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'再次输入新密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证新的密码是否一致
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        return old_password
