from __future__ import unicode_literals

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagefield.fields import ImageField


class MetaMixin(models.Model):
    meta_title = models.CharField(
        _("title"),
        max_length=200,
        blank=True,
        help_text=_("Used for Open Graph and other meta tags."),
    )
    meta_description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("Override the description for this page."),
    )
    meta_image = ImageField(
        _("image"),
        blank=True,
        auto_add_fields=True,
        upload_to="meta/%Y/%m",
        help_text=_("Set the Open Graph image."),
        formats={"recommended": ("default", ("crop", (1200, 630)))},
    )
    meta_video_url = models.URLField(
        _("video url"), blank=True, help_text=_("Set the Open Graph video to an url."),
    )
    meta_video = models.FileField(
        _("video"),
        blank=True,
        upload_to="meta/video/%Y/%m",
        help_text=_("Set the Open Graph video."),
        validators=[FileExtensionValidator(["mp4"])],
    )
    meta_video_width = models.IntegerField(_("video width"), default=1920,)
    meta_video_height = models.IntegerField(_("video height"), default=1080,)
    meta_card_type = models.CharField(
        _("twitter card type"),
        blank=True,
        max_length=50,
        choices=(
            (_("summary"), "summary"),
            (_("summary large image"), "summary_large_image"),
            (_("player"), "player"),
        ),
        help_text=_("Card type"),
    )
    meta_twitter_site = models.CharField(
        _("twitter site"),
        blank=True,
        max_length=30,
        help_text=_("The Twitter @username the card should be attributed to."),
    )
    meta_player_width = models.IntegerField(_("player width"), default=1920,)
    meta_player_height = models.IntegerField(_("player height"), default=1080,)
    meta_player = models.CharField(
        _("player url"),
        blank=True,
        max_length=600,
        help_text=_("HTTPS URL to iFrame player."),
    )
    meta_canonical = models.URLField(
        _("canonical URL"),
        blank=True,
        help_text=_("If you need this you probably know."),
    )
    meta_author = models.CharField(
        _("author"),
        max_length=200,
        blank=True,
        help_text=_("Override the author meta tag."),
    )
    meta_robots = models.CharField(
        _("robots"),
        max_length=200,
        blank=True,
        help_text=_("Override the robots meta tag."),
    )

    class Meta:
        abstract = True

    @classmethod
    def admin_fieldset(cls, **kwargs):
        cfg = {
            "fields": (
                "meta_title",
                "meta_description",
                "meta_image",
                "meta_image_ppoi",
                "meta_video",
                "meta_video_width",
                "meta_video_height",
                "meta_twitter_site",
                "meta_card_type",
                "meta_player",
                "meta_video_width",
                "meta_player_height",
                "meta_canonical",
                "meta_author",
                "meta_robots",
            ),
            "classes": ("tabbed",),
        }
        cfg.update(kwargs)
        return (_("Meta tags"), cfg)

    def meta_dict(self):
        ctx = {
            "title": self.meta_title or getattr(self, "title", ""),
            "description": self.meta_description,
            "canonical": self.meta_canonical,
            # Override URL if canonical is set to a non-empty value (the empty
            # string will be skipped when merging this dictionary)
            "url": self.meta_canonical,
            "author": self.meta_author,
            "robots": self.meta_robots,
        }
        ctx.update(self.meta_images_dict())
        ctx.update(self.meta_video_dict())
        return ctx

    def meta_images_dict(self):
        if self.meta_image:
            return {
                "image": str(self.meta_image.recommended),
                "image:width": 1200,
                "image:height": 630,
            }

        elif getattr(self, "image", None):
            return {"image": self.image.url}

        return {"image": ""}

    def meta_video_dict(self):
        if self.meta_video:
            return {
                "video": self.meta_video.url,
                "video:width": self.meta_video_width,
                "video:height": self.meta_video_height,
            }
        if self.meta_video:
            return {
                "video": self.meta_video_url,
                "video:width": self.meta_video_width,
                "video:height": self.meta_video_height,
            }
        return {}
