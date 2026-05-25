import hashlib

from django.core.cache import cache


PROPERTY_CACHE_VERSION_KEY = "properties:cache_version"


def get_property_cache_version():
    version = cache.get(PROPERTY_CACHE_VERSION_KEY)

    if version is None:
        version = 1
        cache.set(PROPERTY_CACHE_VERSION_KEY, version, None)

    return version


def bump_property_cache_version():
    # Tang version de cac cache key cu tu dong bi bo qua.
    # Cach nay don gian hon viec phai delete tung key theo query params.
    version = get_property_cache_version() + 1
    cache.set(PROPERTY_CACHE_VERSION_KEY, version, None)
    return version


def make_property_cache_key(name, query_params):
    # Query params co the khac nhau: ?district=...&min_price=...
    # Nen cache key can dua tren toan bo query string.
    version = get_property_cache_version()
    raw_query = query_params.urlencode()
    query_hash = hashlib.md5(raw_query.encode("utf-8")).hexdigest()

    return f"properties:v{version}:{name}:{query_hash}"
