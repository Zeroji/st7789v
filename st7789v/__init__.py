from .display import Display
try:
    from .buffered_display import BufferedDisplay
except ImportError:
    pass
