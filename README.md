Python email normalizer
-----------------------

## Usage

```python
from email_normalizer import normalize

# returns alicetestemail@gmail.com
normalize('Alice.Test.Email+2e16f5091e4c9a1fecd712ad1e019569@gmail.com')
```

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
