from setuptools import setup, find_packages

setup(
    name='streamlit_bls_connection',
    version='0.1',
    description='A package to fetch Bureau of Labor Statistics data using Streamlit',
    author='Tony Hollaar',
    author_email='thollaar@gmail.com',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'requests',
        'pandas',
    ],
)
