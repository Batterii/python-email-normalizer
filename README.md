Python email normalizer
-----------------------

## Usage

```python
from email_normalizer import normalize

# returns alicetestemail@gmail.com
normalize('Alice.Test.Email+2e16f5091e4c9a1fecd712ad1e019569@gmail.com')
```

### Default normalizer

The default normalizer can be overridden if you want to specify your own behavior.

```python
from email_normalizer import normalize, BaseNormalizer

class MyNormalizer(BaseNormalizer):
    @classmethod
    def normalize(cls, local_part, domain):
        local_part = local_part.split('--')[0]
        return '{0}@{1}'.format(local_part, domain)

# returns bob@cipher.com
normalize('Bob--Test@cipher.com', default_normalizer=MyNormalizer)
```

### Registering / Unregistering normalizers

3rd party normalizers can be registered and unregistered to provide alternate behavior for known domains.

```python
from email_normalizer import normalize, register_normalizer, \
    unregister_normalizer, BaseNormalizer

class FooBarNormalizer(BaseNormalizer):
    domains = ['foobar.com']

    @classmethod
    def normalize(cls, local_part, domain):
        local_part = local_part.split('--')[0]
        return '{0}@{1}'.format(local_part, domain)

# register the normalizer for foobar.com
register_normalizer(FooBarNormalizer)

# returns bob@cipher.com
normalize('Bob--Test@cipher.com')

# unregister the normalizer for foobar.com
unregister_normalizer(FooBarNormalizer)

# returns bob--test@cipher.com
normalize('Bob--Test@cipher.com')
```

## Running tests

```python
# The first run will fetch requirements / dependencies
python setup.py test
```
