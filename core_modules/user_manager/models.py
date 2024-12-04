from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, phone, password=None):
        if email is None:
            raise TypeError(_('Users must have an email address'))

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.phone = phone
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Inserisci password')
        user = self.create_user(username, email, None, None, None, "Persona Fisica", password)
        user.is_superuser = True
        user.is_staff = True
        user.permission = 100
        user.is_verified = True
        user.save()
        return user


# User Levels - Removed due to the usage of PermissionsMixin
# USER_LEVEL = (
#     (100, "SuperAdmin"),
#     (50, "Admin"),
#     (1, "Utente"),
# )

# User Types - Removed due to the usage of PermissionsMixin
# USER_TYPE_CHOICES = (
#     ('Persona Fisica', 'Persona Fisica'),
#     ('Azienda', 'Azienda'),
#     ('NoProfit', 'Ente No Profit'),
# )


class User(AbstractBaseUser, PermissionsMixin):
    
    # Base information 
    username = models.CharField(max_length=40, validators=[MinLengthValidator(4)], null=True, blank=True)
    email = models.CharField(max_length=70, validators=[MinLengthValidator(4)], unique=True, db_index=True)
    
    # System flag
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False) #Removed due to existence in the PermissionsMixin class
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Permissions - Removed due to the usage of Groups and PermissionsMixin
    # permission = models.PositiveSmallIntegerField(verbose_name="Livello permessi utente", default=1, choices=USER_LEVEL)
    # user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES, default='Persona Fisica')

    # Profile fields
    first_name = models.CharField(verbose_name=_("Name"), max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name=_("Surname"), max_length=50, blank=True, null=True)
    fiscal_code = models.CharField(verbose_name=_("Fiscal Code"), max_length=16, blank=True, null=True)
    phone = models.CharField(verbose_name=_("Phone"), max_length=12, blank=True, null=True)
    mobile = models.CharField(verbose_name=_("Mobile"), max_length=12, blank=True, null=True)

    # Model options
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.email)

    def get_name(self):
        return ("{} {}".format(self.first_name, self.last_name))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('last_name',)


