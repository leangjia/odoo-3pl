from . import models

# Conditionally import tests to avoid dependency issues
try:
    from . import tests
except ImportError:
    pass