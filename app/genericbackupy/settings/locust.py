from .development import *
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '300000000000/minute',
    'user': '200000000000/minute'
}
