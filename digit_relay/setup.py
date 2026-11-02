import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'digit_relay'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # daftarkan launch file biar ikut ke-install
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tsakuya',
    maintainer_email='gusdedimas89@gmail.com',
    description='Distributed Digit Relay di turtlesim (tugas ROS2 kelompok 6).',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'member1 = digit_relay.member1:main',
            'member2 = digit_relay.member2:main',
            'member3 = digit_relay.member3:main',
            'member4 = digit_relay.member4:main',
            'member5 = digit_relay.member5:main',
            'member6 = digit_relay.member6:main',
        ],
    },
)
