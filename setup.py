from setuptools import setup

setup(
    name='wilde',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        wilde=main:find_music_in_file
    ''',
)
