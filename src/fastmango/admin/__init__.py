# FastMango Admin Module
"""
Django-style admin interface for FastMango applications.

Provides automatic admin interface generation for FastMango models
with minimal configuration required.
"""

from .base import FastMangoAdmin
from .views import ModelAdmin

__all__ = ["FastMangoAdmin", "ModelAdmin"]