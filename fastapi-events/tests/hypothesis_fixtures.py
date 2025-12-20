"""!WARN: not working file"""
import os

from hypothesis import Verbosity, settings

settings.register_profile(
    "ci",
    settings(
        max_examples=100,
        suppress_health_check=[settings.HealthCheck.too_slow],
        verbosity=Verbosity.quiet,
    ),
)
settings.register_profile(
    "dev",
    settings(
        max_examples=100,
        suppress_health_check=[settings.HealthCheck.too_slow],
        verbosity=Verbosity.verbose,
    ),
)


settings.load_profile(os.getenv("TESTS__HYPOTHESIS_PROFILE", "dev"))
