import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='iertools',
    version='0.3.2',
    author='Guillermo Barrios',
    author_email='gbv@ier.unam.mx',
    description='New Package fitted for Energy Building Group (GEE)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AltamarMx/geetools',
    project_urls = {
        "Bug Tracker": "https://github.com/AltamarMx/geetools/issues"
    },
    license='MIT',
    packages=['iertools'],
    install_requires=['requests','pandas','numpy','datetime'],
)
