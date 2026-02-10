import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'kare_robotu'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Burası launch dosyalarını yükler:
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        # Burası URDF dosyalarını yükler:
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='serkan-sevmez',
    maintainer_email='serkan-sevmez@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'kare_cizici = kare_robotu.kare_cizici:main',
        ],
    },
)
