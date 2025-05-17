try:
    from ._version import version as __version__  # type: ignore
except ImportError:
    __version__ = "0.0.0+unknown"

from .entry import *
from .reader import *
from .compressor import *
from .cli import *
from .set import *
