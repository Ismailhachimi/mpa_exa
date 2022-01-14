from django.db import models
from django.conf import settings
from django.utils.translation import gettext, ugettext_lazy as _
from django.template.defaultfilters import date
from django.db.models.functions import Now
from django.core.exceptions import ValidationError


class Event(models.Model):
    client = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("client"),
        related_name="client",
    )
    expert = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("expert"),
        related_name="expert",
    )

    main_start = models.DateTimeField(
        verbose_name=_("official start"),
        help_text=_(
            "Start time should be in the future and before the end time.")
    )
    main_end = models.DateTimeField(
        verbose_name=_("official end"),
        help_text=_("End time should be in the futur and after the start time.")
    )
    start = models.DateTimeField(
        null=True,
        verbose_name=_("started on"),
        help_text=_(
            "Start time should be in the future and before the end time.")
    )
    end = models.DateTimeField(
        null=True,
        verbose_name=_("ended on"),
        help_text=_("End time should be in the futur and after the start time.")
    )

    title = models.CharField(verbose_name=_("title"), max_length=255)
    description = models.TextField(verbose_name=_("description"))

    created_on = models.DateTimeField(
        verbose_name=_("created on"),
        auto_now_add=True
    )
    updated_on = models.DateTimeField(
        verbose_name=_("updated on"),
        auto_now=True
    )

    def __str__(self):
        return gettext("%(title)s: %(start)s - %(end)s") % {
            "title": self.title,
            "start": date(self.main_start, 'd/m/Y-h:iA'),
            "end": date(self.main_end, 'd/m/Y-h:iA'),
        }

    @ property
    def seconds(self):
        return (self.end - self.start).total_seconds()

    @ property
    def minutes(self):
        return float(self.seconds) / 60

    @ property
    def hours(self):
        return float(self.seconds) / 3600

    def get_absolute_url(self):
        return reverse("event", args=[self.id])

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        # TODO : add contraint
        # only half our dividable ? difference end-start
        # you can make a reservation at least one hour before the start
        # Check NOW(), maybe replace by datetime.now(tz) if POSSIBLE
        constraints = [
            models.CheckConstraint(
                check=models.Q(main_start__lte=models.F(
                    'main_end'), main_start__gte=Now()),
                name='correct_datetime'
            ),
        ]
