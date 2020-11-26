from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='wilde',
    version='0.1',
    setup_requires=['pybind11>=2.2', 'Cython>=0.29'],
    packages=find_packages(),
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        wilde=wilde.main:find_music_in_file
    ''',
    url='https://github.com/wvanlit/wilde'
)
