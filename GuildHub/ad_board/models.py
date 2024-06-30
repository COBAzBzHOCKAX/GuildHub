from datetime import timedelta
import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField

User = get_user_model()


class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'), help_text=_('Enter your title here'))
    text = QuillField(verbose_name=_('Text'), help_text=_('Enter your text here'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    is_published = models.BooleanField(default=False, verbose_name=_('Is published'))
    date_published = models.DateTimeField(null=True, blank=True, verbose_name=_('Date of publication'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    date_of_change = models.DateTimeField(auto_now=True, verbose_name=_('Date of change'))

    class Meta:
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['user']),
        ]
        permissions = [
            ('view_unpublished_ad', 'Can view unpublished ads'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])

    def published_within_the_last_30_days(self):
        """
        Check if the advertisement was published within the last 30 days.
        Returns:
            bool: True if the advertisement was published within the last 30 days, False otherwise.
        """
        logger = logging.getLogger('ad_board.models.Ad.published_within_the_last_30_days')
        logger.debug('launching')

        if self.date_published:
            if timezone.now() - self.date_published <= timedelta(days=30):
                logger.debug(f'Ad {self.id} was published within the last 30 days. \n'
                             f'It was published at {(self.date_published).strftime("%Y-%m-%d %H:%M:%S")}.\n')
                return True

            logger.debug(f'Ad {self.id} was posted more than 30 days ago. \n'
                         f'It was published at {(self.date_published).strftime("%Y-%m-%d %H:%M:%S")}.\n')
        else:
            logger.debug(f'Ad {self.id} has no publication date')

        return False

    def date_of_publication(self):
        """
        Set the publication date if the advertisement is published and date_published is not set.

        If the advertisement is marked as published (`is_published` is True) and `date_published`
        is not set, this method sets `date_published` to the current time in UTC (`timezone.now()`).

        This method ensures that advertisements are not artificially pushed to the top of the ad board
        by re-publishing them within 30 days. Ads can only be republished and thus moved to the top of the
        list after 30 days.
        """
        logger = logging.getLogger('ad_board.models.Ad.date_of_publication')
        logger.debug('launching')

        if self.is_published and not self.published_within_the_last_30_days():
            self.date_published = timezone.now()
            logger.debug(f'For the announcement {self.id} the publication date was set {self.date_published}.\n')
        else:
            logger.debug(f'The conditions for setting a new date for the '
                         f'publication of the announcement are not met {self.id}. \n'
                         f'is_published = {self.is_published} \n'
                         f'published_within_the_last_30_days = {self.published_within_the_last_30_days()}\n')

    def publish_ad(self):
        """Publish the advertisement."""
        logger = logging.getLogger('ad_board.models.Ad.publish_ad')
        logger.debug('launching')

        self.is_published = True
        self.date_of_publication()
        self.save()
        logger.debug(f'Ad {self.id} was published.\n')

    def unpublish_ad(self):
        """Unpublish the advertisement."""
        logger = logging.getLogger('ad_board.models.Ad.unpublish_ad')
        logger.debug('launching')

        self.is_published = False
        self.save()
        logger.debug(f'Ad {self.id} was unpublished.\n')

    def short_title(self):
        """Return the first 50 characters of the title."""
        if len(self.title) > 50:
            return self.title[:50] + '...'
        return self.title

    def short_text(self):
        """Return the first 50 characters of the text."""
        if len(self.text) > 50:
            return self.text[:50] + '...'
        return self.text

    def save(self, *args, **kwargs):
        self.date_of_publication()  # Set publication date on save
        super().save(*args, **kwargs)

    def can_view(self, user):
        """Check if user can view the ad."""
        logger = logging.getLogger('ad_board.models.Ad.can_view')
        logger.debug('launching')

        # Check if the ad is published
        if self.is_published:
            logger.debug(f'Ad {self.id} is published\n')
            return True

        # Check if the ad is owned by the user
        if user.is_authenticated and user == self.user:
            logger.debug(f'Ad {self.id} is owned by {user}\n')
            return True

        # Check if the user has permission to view unpublished ads
        if user.is_staff:
            logger.debug(f'User {user} is staff\n')
            return True

        # Check if the user has permission to view unpublished ads
        if user.is_superuser:
            logger.debug(f'User {user} is superuser\n')
            return True

        # Check if the user has permission to view unpublished ads
        if user.has_perm('ad_board.view_unpublished_ad'):
            logger.debug(f'User {user} has view_unpublished_ad permission\n')
            return True

        logger.debug(f'User {user} cannot view the ad {self.id}\n')
        return False


class Category(models.Model):
    category_name = models.CharField(
        unique=True,
        max_length=255,
        verbose_name=_('Category name'),
        help_text=_('Enter your category name here'),
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.category_name
