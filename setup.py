from setuptools import setup

setup(
    name='infinite_list',
    version='0.1.0',
    packages=[''],
    url='https://github.com/charlie572/infinite_list',
    license='',
    author='Charlie',
    author_email='barehamcharlie@gmail.com',
    description='An infinite list data structure',
    install_requires = [
        'binary_search_tree @ git+https://github.com/charlie572/binary_search_tree.git',
    ],
)
