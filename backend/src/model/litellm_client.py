import warnings

import litellm

# Suppress aiohttp deprecation warning on Python 3.13+
warnings.filterwarnings(
    "ignore", message="enable_cleanup_closed", category=DeprecationWarning
)

# Disable litellm telemetry/logging noise
litellm.suppress_debug_info = True
litellm.set_verbose = False
