from setuptools import setup

package_name = 'opencv_tools'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='focalfossa',
    maintainer_email='automaticaddison@todo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
          'img_publisher = opencv_tools.basic_image_publisher:main',
          'img_subscriber = opencv_tools.basic_image_subscriber:main',
          'aruco_marker_pose_estimator_tf = opencv_tools.aruco_marker_pose_estimation_tf:main',
        ],
    },
)
