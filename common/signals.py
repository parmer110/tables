from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from common.models import BlacklistedToken
from .models import Pictures

@receiver(post_save, sender=Pictures)
def move_record_to_top(sender, instance, **kwargs):
    if instance.classification.name == "profile" and instance.classification.model == "Pictures":
        Pictures.objects.filter(pk=instance.pk).update(id=instance.id-1)


# import pdb; pdb.set_trace()


@receiver(post_save, sender=BlacklistedToken)
def clear_cache_on_blacklist(sender, instance, **kwargs):
    cache_key = f'user:{instance.token}'
    cache.delete(cache_key)
