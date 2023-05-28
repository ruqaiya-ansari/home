from django import template
from accounts.forms import MyAuthForm, UserRegistrationForm

register = template.Library()


@register.inclusion_tag('modal.html')
def account_forms():
    login_form = MyAuthForm()
    registration_form = UserRegistrationForm()
    return {'login': login_form, 'register': registration_form}
