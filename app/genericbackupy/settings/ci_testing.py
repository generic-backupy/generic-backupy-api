from .development import *

# ensure DEBUG is False in Production
DEBUG = True
TEMPLATE_DEBUG = True
SECRET_KEY = '$pbt=4s%9ahb6l=rv3j$zd_my&k8c9+z9u%w+1h!=_=e-!z4!t'

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-html',
    '--cover-xml',
    '--cover-package=api,genericbackupy,gb_packages,gb_module',
]
