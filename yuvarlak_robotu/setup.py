import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'yuvarlak_robotu'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='serkan-sevmez',
    maintainer_email='serkan-sevmez@todo.todo',
    description='Yuvarlak cizen robot projesi',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'yuvarlak_kod = yuvarlak_robotu.yuvarlak_kod:main',
        ],
    },
)
