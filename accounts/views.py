
from django.urls import reverse_lazy
from .models import Profile
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateResponseMixin, View
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login


# Create your views here.

class UserRegistrationView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('browse:search')

    def form_valid(self, form):
        # create the user object
        user = form.save(commit=False)

        cd = form.cleaned_data

        user.set_password(cd["password"])
        # save your User object to the database
        user.save()
        Profile.objects.create(user=user)

        authenticated_user = authenticate(username=cd['username'], password=cd['password'])

        login(self.request, authenticated_user)

        return super(UserRegistrationView, self).form_valid(form)


class Edit(TemplateResponseMixin, View):
    template_name = 'edit.html'

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return self.render_to_response({'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return self.render_to_response({'user_form': user_form, 'profile_form': profile_form})

