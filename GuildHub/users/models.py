from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        """
        Creates a user with the given email and optional password.

        Parameters:
            email (str): The email of the user.
            password (str): The password for the user.
            **kwargs: Additional keyword arguments to create the user.

        Returns:
            User: The created user object.
        """
        if not email:
            raise ValueError(_('Users must have an Email'))

        if not password:
            raise ValueError(_('Users must have a Password'))

        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='Email',
        help_text=_('Enter your email'),
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('First name'),
        help_text=_('Enter your first name'),
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Last name'),
        help_text=_('Enter your last name'),
    )
    nickname = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Nickname'),
        help_text=_('Enter your nickname in the game'),
    )
    avatar = models.ImageField(
        upload_to='avatars',
        blank=True,
        null=True,
        default='default.png',
        verbose_name=_('Avatar'),)
    date_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Date of birth'),
        help_text=_('Enter your date of birth'),
    )
    phone_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Phone number'),
        help_text=_('Enter your phone number'),
    )
    discord_url_profile = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Discord profile URL'),
        help_text=_('Enter your Discord profile URL'),
    )
    about_me = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('About Me'),
        help_text=_('Enter your about me here')
    )
    last_time_visit = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
