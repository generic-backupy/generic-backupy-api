# gb_module

## Build

```
# build it (don't forget to increase the version number)
python3 setup.py sdist bdist_wheel
# install it locally
pip3 install -e .
# upload to pypi
python3 -m twine upload --skip-existing dist/*
```
