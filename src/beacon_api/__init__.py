"""
The ``beacon_api`` package contains code to start an EGA Beacon API.
"""

__title__ = 'Beacon v2.0'
__version__ = VERSION = '2.0'
__author__ = 'CRG developers'
__license__ = 'Apache 2.0'
__copyright__ = 'Beacon 2.0 @ CRG, Barcelona'


# Send warnings using the package warnings to the logging system
# The warnings are logged to a logger named 'py.warnings' with a severity of WARNING.
# See: https://docs.python.org/3/library/logging.html#integration-with-the-warnings-module
import logging
import warnings
logging.captureWarnings(True)
warnings.simplefilter("default")  # do not ignore Deprecation Warnings
