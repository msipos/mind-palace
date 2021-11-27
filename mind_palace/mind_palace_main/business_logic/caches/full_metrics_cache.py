from typing import Optional

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Q

from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_now
from mind_palace.mind_palace_main.models import Collection, Note


def get_full_metrics(user: User, reference_time: Optional[int] = None) -> dict:
    if reference_time is None:
        reference_time = timestamp_now()

    collections = Collection.get_collections(user)
    collection_metrics = []
    for c in collections:
        collection_metrics.append({
            'name': c.name,
            'id': c.id,
            'num_total': Note.objects.filter(collection=c).count(),
            'num_archived': Note.objects.filter(Q(collection=c) & Q(archived=True)).count(),
            'num_active': Note.get_active_notes(c, reference_time).count()
        })
    total_active = sum([cm['num_active'] for cm in collection_metrics])
    return {
        'total_active': total_active,
        'collections': collection_metrics
    }


def get_cached_full_metrics(user: User, reference_time: Optional[int] = None) -> dict:
    cache_key = f'full_metrics_{user.username}'
    out = cache.get(cache_key)
    if out is None:
        out = get_full_metrics(user, reference_time)
        cache.set(cache_key, out, timeout=15*60*60)
    return out


def invalidate_cached_full_metrics(user: User):
    cache.delete(f'full_metrics_{user.username}')
