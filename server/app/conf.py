"""app conf."""

ALLOW_TOKEN = ''
DINGDING_URL = ''

try:
    from .localconf import *
except ImportError:
    pass
