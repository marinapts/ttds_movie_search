from setuptools import setup, find_packages

setup(
    name='ttds_movie_search',
    packages=find_packages(include=['db', 'db.*']),
    python_requires='>=3.6'
)
