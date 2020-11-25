from setuptools import setup, find_packages

setup(
    name='wilde',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
        'pydub',
        'inaSpeechSegmenter',
    ],
    entry_points='''
        [console_scripts]
        wilde=wilde.main:find_music_in_file
    ''',
    url='https://github.com/wvanlit/Wilde'
)
