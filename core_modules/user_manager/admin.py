# -*- coding: utf-8 -*-
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import admin
from django.contrib.auth.forms import forms
from django.core.validators import validate_email as email_re
from django.utils.translation import gettext_lazy as _

from .models import User


class ProfileAddForm(forms.ModelForm):
    error_messages = {
        "duplicate_email": _("A user with this e-mail address already exists."),
        "password_mismatch": _("The two password fields didn't match."),
        "not_email": _("Email is not valid"),
    }
    email = forms.RegexField(
        label=_("E-mail"),
        max_length=75,
        regex=r"^[\w.@+-]+$",
        help_text=_("Required 75 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={"invalid": _("This value may contain only letters, numbers and " "@/./+/-/_ characters.")},
    )
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            email = str(email).lower()
        except Exception as E:
            print(_("Error while formatting email: %s") % E)
        try:
            user_already_exist = User.objects.get(email=email, deleted=False)
            if user_already_exist:
                forms.ValidationError(self.error_messages["duplicate_email"])
        except Exception:
            email_re(email)
            return email
        raise forms.ValidationError(self.error_messages["not_email"])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(self.error_messages["password_mismatch"])
        return password2

    def save(self, commit=True):
        user = super(ProfileAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (("first_name", "last_name", "phone", "fiscal_code"),),
            },
        ),
        (
            _("Permissions"),
            {"fields": ("permission", "is_superuser", "is_active", "is_staff")},
        ),
    )

    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        else:
            return self.fieldsets

    list_display = (
        "email",
        "first_name",
        "last_name",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("last_name",)
    add_form = ProfileAddForm
    # change_password_form = AdminPasswordChangeForm
    # form = ProfileChangeForm


admin.site.register(User, UserAdmin)
