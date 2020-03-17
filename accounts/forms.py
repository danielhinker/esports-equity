from django.contrib.auth import get_user_model, authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

# from django.contrib.auth.models import User

from django import forms
from django.forms import ModelForm
from .models import *
from teams.models import *

from django.core import validators


class UserCreateForm(UserCreationForm):
    # email = forms.EmailField(label="Email address", required=True)

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'tos_not_accepted': _("You must accept the Terms of Service in order to register."),
        'username_taken': _("This username is already taken."),
    }

    class Meta:
        fields = ("first_name", "last_name", "username", "password1", "password2",
                  "accepted_tos", "is_subscribed",)
        labels = {"is_subscribed": "Subscribe to our E-mail Newsletter",
                  "accepted_tos": "Do you accept the {}?".format('<a href="/TermsofService/">Terms of Service</a>'),
                  # "is_accredited": "Check if you are an Accredited Investor",
                  }

        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['accepted_tos'].required = True
        # self.fields["username"].label = "Display name"
        self.fields["username"].label = "Email address"

    def clean(self):
        # To keep the main validation and error messages
        super().clean()
        username = self.cleaned_data['username']
        lowercase_username = username.lower()
        User = get_user_model()
        # Now it's time to add your custom validation
        if self.cleaned_data['accepted_tos'] is False and User.objects.filter(username=lowercase_username).exists():
            self.add_error('accepted_tos', self.error_messages['tos_not_accepted'])
            self.add_error('username', self.error_messages['username_taken'])
        elif self.cleaned_data['accepted_tos'] is False:
            self.add_error('accepted_tos', self.error_messages['tos_not_accepted'])
            # self._errors['accepted_tos'] = ' '
            # raise forms.ValidationError(
            #     self.error_messages['tos_not_accepted'],
            #     code='tos_not_accepted',
            # )
        elif User.objects.filter(username=lowercase_username).exists():
            # self._errors['username'] = ' '
            self.add_error('username', self.error_messages['username_taken'])
            # raise forms.ValidationError(
            #     self.error_messages['username_taken'],
            #     code='username_taken',
            # )
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        lowercase_username = self.cleaned_data['username']
        user.username = lowercase_username.lower()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    # avatar = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio', 'company_name',
                  'is_subscribed','avatar']
        labels = {'is_subscribed':'Newsletters', 'bio':'About You'}






# class ChangeSettings(forms.ModelForm):
#     # first_name = forms.CharField(label="First Name", required=True)
#     # last_name = forms.CharField(label="Last Name", required=True)
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         try:
#             self.fields['email'].initial = self.instance.user.email
#         except User.DoesNotExist:
#             pass
#
#     class Meta:
#         model = get_user_model()
#         fields = ("first_name", "last_name")




    # def save(self, *args, **kwargs):
    #     """
    #     Update the first name, last name, and bio on the related User object
    #     """
    #     user = self.instance.user
    #     user.first_name = self.cleaned_data["first_name"]
    #     user.last_name = self.cleaned_data["last_name"]
    #     user.bio = self.cleaned_data["bio"]
    #     user.save()
    #     profile = super().save(*args, **kwargs)
    #     return profile



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["email"].label = "Email address"
    #
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError(
    #             self.error_messages['password_mismatch'],
    #             code='password_mismatch',
    #         )
    #     lowercase_username = self.cleaned_data.get('username')
    #     self.instance.username = lowercase_username
    #     password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
    #     return password2


# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, request=None, *args, **kwargs):
#         """
#         The 'request' parameter is set for custom auth use by subclasses.
#         The form data comes in via the standard 'data' kwarg.
#         """
#         self.request = request
#         self.user_cache = None
#         super(AuthenticationForm, self).__init__(*args, **kwargs)
#
#         # Set the label for the "username" field.
#         UserModel = get_user_model()
#         self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
#         if self.fields['username'].label is None:
#             self.fields['username'].label = capfirst(self.username_field.verbose_name)
#
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         return username.lower
#
#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         username.lower()
#
#         if username and password:
#             self.user_cache = authenticate(username=username, password=password)
#             if self.user_cache is None:
#                 raise forms.ValidationError(
#                     self.error_messages['invalid_login'],
#                     code='invalid_login',
#                     params={'username': self.username_field.verbose_name},
#                 )
#             else:
#                 self.confirm_login_allowed(self.user_cache)
#
#         return self.cleaned_data

class ProjectCreateForm2(forms.ModelForm):
    # short_description = forms.CharField(widget=forms.Textarea(attrs={'id':'tinymce_short'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'id':'title-input'}))
    short_description = forms.CharField(widget=forms.Textarea(attrs={'id':'description-input'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['project_image'].required = True
        self.fields['title'].required = True
        # self.fields['project_category'].required = True
        # self.fields['project_location'].required = False
        # self.fields['short_description'].required = True
        # self.fields['gaming_category'].required = False
        # self.fields['duration'].required = True
        # self.fields['funding_goal'].required = False

    class Meta:
        model = Team
        fields = ['project_image', 'title', 'short_description', 'project_category', 'project_location',
                  'duration', 'funding_goal',]
        labels = {
            'title': 'What is your team name?',
            'project_category': 'Which game are you fundraising for?',
            'short_description': 'Tell us more about your project',
            # 'gaming_category': 'Which game are you fundraising in?',
            'duration': 'When do you want to end your project?',
            'funding_goal': 'How much are you trying to raise?',
        }


class ProjectCreateForm3(forms.ModelForm):
    project_description = forms.CharField(widget=forms.Textarea(attrs={'id':'tinymce_description'}))
    project_story_background = forms.CharField(widget=forms.Textarea(attrs={'id':'tinymce_story'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project_description'].required = True
        self.fields['project_story_background'].required = True

    class Meta:
        model = Team
        fields = ['project_video', 'project_description', 'project_story_background']
        labels = {
            'project_description': 'Tell the community more about your project',
            'project_story_background': 'Mention risks or challenges you have come across',
        }


class ProjectCreateForm4(forms.ModelForm): #TODOITEM
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['project_description'].required = True
        # self.fields['project_story_background'].required = True
    reward_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Reward
        fields = ['reward_title', 'reward_amount', 'reward_description',
                  'estimated_delivery', 'shipping_details']
        labels = {
            'project_description': 'Tell the community more about your project',
            'project_story_background': 'Mention risks or challenges you have come across',
        }

# class TestCreateForm(forms.ModelForm):
#     class Meta:
#         model = TestCreateForm
#         fields = ['test_title']


# class TodoListForm(forms.ModelForm):
#     class Meta:
#         model = TodoList
#         exclude=()
#
# class TodoItemForm(forms.ModelForm):
#     class Meta:
#         model = TodoItem
#         exclude=('list',)

class BackProjectForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['amount'].required = True

    class Meta:
        model = Backing
        fields = ['amount']
        labels = {
            'amount': 'How much do you want to back this project?',
            'message': 'Do you want to leave a message?',
        }
# class ProjectCreateFormset4(forms.ModelForm):
#     class Meta:
#         model = Team
#         exclude = ()
#
#
#         # FamilyMemberFormSet = inlineformset_factory(Project, Reward,
#         #                                             form=ProjectCreateForm4, extra=1)



class ProjectCreateForm5(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['project_description'].required = True
        # self.fields['project_story_background'].required = True

    class Meta:
        model = Team
        fields = ['profile_image', 'profile_biography',
                  ]
        labels = {
            'project_description': 'Tell the community more about your project',
            'project_story_background': 'Mention risks or challenges you have come across',
        }

class ProjectCreateForm6(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['project_description'].required = True
        # self.fields['project_story_background'].required = True

    class Meta:
        model = BankAccount
        fields = ['contact_email', 'firstName', 'lastName', 'dob_day',
                  'dob_month', 'dob_year', 'address1', 'city',
                  'zip', 'country', 'routing_number', 'account_number']
        labels = {
            'address1': 'Address',
            'city1': 'City',
            'zip': 'Zip Code',
            'country': 'Country',
        }


class PickyAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("Activate your account before logging in."),
                code='inactive',
            )
        if user.username.startswith('b'):
            raise forms.ValidationError(
                _("Sorry, accounts starting with 'b' aren't welcome here."),
                code='no_b_users',
            )