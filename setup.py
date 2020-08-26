from setuptools import setup, find_packages

setup(
    name="url-shortener",
    description="A url shortener made for learning",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["flask", "flask-sqlalchemy", "psycopg2", "python-dotenv", "python-dateutil", "gunicorn"],
)
