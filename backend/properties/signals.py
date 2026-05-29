from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .cache_utils import bump_property_cache_version
from .models import Property


@receiver(post_save, sender=Property)
def clear_property_cache_after_save(sender, instance, **kwargs):
    bump_property_cache_version()


@receiver(post_delete, sender=Property)
def clear_property_cache_after_delete(sender, instance, **kwargs):
    bump_property_cache_version()


@receiver(m2m_changed, sender=Property.amenities.through)
def clear_property_cache_after_amenities_change(sender, instance, **kwargs):
    bump_property_cache_version()
