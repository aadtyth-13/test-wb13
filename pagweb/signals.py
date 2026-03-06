#tomakesure media will be deleted when replace
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from .models import T_Event, T_Product, T_Church, T_Staff, T_EventMedia

def _delete_old_file(sender, instance, field_name: str):
    if not instance.pk:
        return
    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    old_file = getattr(old, field_name)
    new_file = getattr(instance, field_name)
    if old_file and old_file != new_file:
        old_file.delete(save=False)

@receiver(pre_save, sender=T_Event)
def event_delete_old_image(sender, instance, **kwargs):
    _delete_old_file(sender, instance, "main_image")

@receiver(pre_save, sender=T_Product)
def product_delete_old_image(sender, instance, **kwargs):
    _delete_old_file(sender, instance, "main_image")

@receiver(pre_save, sender=T_Church)
def church_delete_old_image(sender, instance, **kwargs):
    _delete_old_file(sender, instance, "main_image")

@receiver(pre_save, sender=T_Staff)
def staff_delete_old_image(sender, instance, **kwargs):
    _delete_old_file(sender, instance, "photo")

@receiver(post_delete, sender=T_Event)
def event_delete_image(sender, instance, **kwargs):
    if instance.main_image:
        instance.main_image.delete(save=False)

@receiver(post_delete, sender=T_Product)
def product_delete_image(sender, instance, **kwargs):
    if instance.main_image:
        instance.main_image.delete(save=False)

@receiver(post_delete, sender=T_Church)
def church_delete_image(sender, instance, **kwargs):
    if instance.main_image:
        instance.main_image.delete(save=False)

@receiver(post_delete, sender=T_Staff)
def staff_delete_image(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(save=False)

@receiver(pre_save, sender=T_EventMedia)
def event_media_delete_old_image(sender, instance, **kwargs):
    _delete_old_file(sender, instance, "image")

@receiver(post_delete, sender=T_EventMedia)
def event_media_delete_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)