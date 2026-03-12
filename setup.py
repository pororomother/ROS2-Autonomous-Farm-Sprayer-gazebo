import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'new_gazebo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        # --- THESE LINES COPY ALL YOUR FILES OVER ---
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
        # --------------------------------------------
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tey',
    maintainer_email='tey@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = new_gazebo.my_node:main'
        ],
    },
)