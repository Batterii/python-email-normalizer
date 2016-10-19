# encoding: utf-8
import logging
from dns import resolver
from dns.exception import DNSException

from .base import BaseNormalizer
from .default import DefaultNormalizer

from .google import GoogleNormalizer
from .fastmail import FastMailNormalizer
from .microsoft import MicrosoftNormalizer
from .yahoo import YahooNormalizer
from .yandex import YandexNormalizer
from .rambler import RamblerNormalizer

logger = logging.getLogger(__name__)

__all__ = [
    'normalize',
]


NORMALIZERS = (
    GoogleNormalizer,
    FastMailNormalizer,
    MicrosoftNormalizer,
    YahooNormalizer,
    YandexNormalizer,
    RamblerNormalizer
)


_domain_normalizers = {}


def register_normalizer(normalizer_cls):
    assert issubclass(normalizer_cls, BaseNormalizer)
    for domain in normalizer_cls.domains:
        if domain in _domain_normalizers:
            raise ValueError('Duplicated domain value %s for normalizer %s', domain, normalizer_cls)

        _domain_normalizers[domain] = normalizer_cls


def unregister_normalizer(normalizer_cls):
    assert issubclass(normalizer_cls, BaseNormalizer)
    for domain in normalizer_cls.domains:
        if domain not in _domain_normalizers:
            raise ValueError('Domain value %s for normalizer %s was not previously registered', domain, normalizer_cls)

        del _domain_normalizers[domain]


def _load_normalizers():
    for cls in NORMALIZERS:
        register_normalizer(cls)


def _get_mx_servers(domain):
    try:
        answer = resolver.query(domain, 'MX')
        return [str(record.exchange).lower()[:-1] for record in answer]
    except DNSException as error:
        logger.error('DNS error for %s: %r', domain, error)
        return []


def _get_normalizer(domain, resolve, default_normalizer):
    if domain in _domain_normalizers:
        return _domain_normalizers[domain]

    if resolve:
        for mx in _get_mx_servers(domain):
            for service_domain, normalizer in _domain_normalizers.iteritems():
                if mx.endswith(service_domain):
                    return normalizer

    return default_normalizer or DefaultNormalizer


def normalize(email, resolve=True, default_normalizer=None):
    local_part, domain = email.lower().split('@')

    return _get_normalizer(domain, resolve, default_normalizer).normalize(local_part, domain)


_load_normalizers()
