from .trie import Trie
from products.models import Product

trie = Trie()

def load_trie():
    for name in Product.objects.values_list('name', flat=True):
        trie.insert(name)

def autocomplete(prefix):
    return trie.search_prefix(prefix)
