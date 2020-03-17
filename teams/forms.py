from django import forms
from .models import *
from django.views import generic
from django.utils.translation import ugettext as _
import datetime
from accounts.models import Follow

class TeamListView(generic.ListView):
    model = Team
    template_name = 'teams/team_list.html'


class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class ProjectCreateForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields["title"].label = "Project Title"
        self.fields['project_category'].required = True
        self.fields['project_location'].required = True

    error_messages = {
        'project_taken': _("This project title is already taken."),
    }

    class Meta:
        model = Team
        fields = ['title', 'project_category', 'project_location',]
        labels = {
            'title': 'Give your project a title:',
            'project_category': _('Select a category:'),
            'project_location': _('Choose your state of residence:'),
        }

    def clean(self):
        # To keep the main validation and error messages
        super().clean()
        title = self.cleaned_data['title']
        lowercase_title = title.lower()

        if Team.objects.filter(title=lowercase_title).exists():
            self.add_error('title', self.error_messages['project_taken'])
        return self.cleaned_data



class ProjectCreateForm2(forms.ModelForm):

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project_image'].required = True
        self.fields['title'].required = True
        self.fields['project_category'].required = True
        self.fields['project_location'].required = True
        self.fields['short_description'].required = True
        self.fields['duration'].required = True
        self.fields['funding_goal'].required = True

    title = forms.CharField(widget=forms.TextInput(attrs={'id': 'title-input'}))
    short_description = forms.CharField(widget=forms.Textarea(attrs={'id': 'description-input'}))


    class Meta:
        model = Team
        fields = ['project_image', 'title', 'short_description', 'project_category', 'project_location',
                  'duration', 'funding_goal',]



class ProjectCreateForm3(forms.ModelForm):
    project_description = forms.CharField(widget=forms.Textarea(attrs={'id':'tinymce_description'}))
    project_story_background = forms.CharField(widget=forms.Textarea(attrs={'id':'tinymce_story'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project_description'].required = True
        self.fields['project_story_background'].required = True

    class Meta:
        model = Team
        fields = ['project_video', 'project_image_2', 'project_description', 'project_story_background']
        labels = {
            'project_description': 'Tell the community more about your project',
            'project_story_background': 'Mention risks or challenges you have come across',
        }


class ProjectCreateForm4(forms.ModelForm): #TODOITEM
    # estimated_delivery = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=SelectDateWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reward_title'].required = True
        self.fields['reward_amount'].required = True
        self.fields['reward_description'].required = True
        self.fields['estimated_delivery'].required = True
        self.fields['shipping_details'].required = True

    class Meta:
        model = Reward
        fields = ['reward_title', 'reward_amount', 'reward_description',
                  'estimated_delivery', 'shipping_details']

        labels = {
            'estimated_delivery': 'MM-DD-YYYY',
            'project_story_background': 'Mention risks or challenges you have come across',
        }


AnswerFormSet = forms.modelformset_factory(
    Reward,
    form=ProjectCreateForm4,
)


AnswerInlineFormSet = forms.inlineformset_factory(
    Team,
    Reward,
    extra=0,
    fields=('reward_title', 'reward_amount', 'reward_description',
            'estimated_delivery', 'shipping_details'),
    formset=AnswerFormSet,
    min_num=1,
)


class BackProjectForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Backing
        fields = ['amount',]
        labels = {
            'amount': 'How much do you want to back this project?',
            'message': 'Do you want to leave a message?',
        }


class ProjectCreateForm5(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].required = True
        self.fields['profile_biography'].required = True

    class Meta:
        model = Team
        fields = ['profile_image', 'profile_biography',
                  ]
        labels = {
            'project_description': 'Tell the community more about your project',
            'project_story_background': 'Mention risks or challenges you have come across',
        }

class ProjectCreateForm6(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_email'].required = True
        self.fields['firstName'].required = True
        self.fields['lastName'].required = True
        self.fields['dob_day'].required = True
        self.fields['dob_month'].required = True
        self.fields['dob_year'].required = True
        self.fields['address1'].required = True
        self.fields['city'].required = True
        self.fields['zip'].required = True
        self.fields['country'].required = True
        self.fields['routing_number'].required = True
        self.fields['account_number'].required = True

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


class FollowCreateForm(forms.ModelForm):

    class Meta:
        model = Follow
        fields = ['user', 'project']

