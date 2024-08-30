import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='iertools',
    version='0.6.6',
    author=['Guillermo Barrios','Efraín Puerto Castellanos'],
    author_email=['gbv@ier.unam.mx','eapc@ier.unam.mx'],
    description='Package to load data from SQL files in EnergyPlus ',
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
