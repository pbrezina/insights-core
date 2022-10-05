"""
This module contains optional, extra datasources that are used by various Red
Hat Insights components.
"""

from insights.core.spec_factory import simple_command, simple_file, SpecSet


class ExtraSpecs(SpecSet):
    neofetch = simple_command("/usr/bin/neofetch --off")
