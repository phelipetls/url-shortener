from setuptools import setup

setup(
    name="url-minifier",
    description="A url shortener made for learning",
    packages=["url-minifier"],
    include_package_data=True,
    install_requires=["flask"],
)
