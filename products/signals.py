from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from search.services import trie

@receiver(post_save, sender=Product)
def update_trie(sender, instance, created, **kwargs):
    trie.insert(instance.name)
