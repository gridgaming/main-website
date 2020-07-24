from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# class Giveaway(models.Model):
#     title = models.CharField(max_length=200)
#     url = models.URLField(max_length=500, unique=True, blank=True, null=True)
#     image = models.ImageField(null=True, blank=True)
#
#     def get_absolute_url(self):
#         return reverse("giveaways:giveaway-detail", args=[str(self.id)])


class Giveaway(models.Model):
    """Uses primary key and slug in URL"""
    title = models.CharField(max_length=settings.GIVEAWAY_TITLE_MAX_LENGTH)
    description = models.TextField(max_length=500, null=True, blank=True)
    giveaway_end_date = models.DateTimeField(null=True, blank=True)
    url = models.URLField(max_length=500, unique=True, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(
        default="", editable=False, max_length=settings.GIVEAWAY_TITLE_MAX_LENGTH
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {"pk": self.id, "slug": self.slug}
        return reverse("giveaways:giveaway-detail", kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
