try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.0.0+unknown"

from .cli import *
from .compressor import *
from .entry import *
from .reader import *
from .set import *
