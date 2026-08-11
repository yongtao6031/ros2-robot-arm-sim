import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'armpy_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zyt',
    maintainer_email='2191345799@qq.com',
    description='No-hardware ROS 2 simulation nodes for the Armpy arm.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'keyboard_node = armpy_sim.keyboard_node:main',
            'mock_arm_node = armpy_sim.mock_arm_node:main',
            'pose_to_joint_states_node = armpy_sim.pose_to_joint_states_node:main',
        ],
    },
)
