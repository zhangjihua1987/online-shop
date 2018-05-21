from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def create_user_fav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delet_user_fav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.fav_num = 0 if goods.fav_num < 0 else goods.fav_num
    goods.save()
