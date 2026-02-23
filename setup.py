from setuptools import setup

package_name = "livox2_to_pc2"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/livox2_to_pc2.launch.py"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="mario-cirtesu",
    maintainer_email="mario@todo.com",
    description="Bridge livox_ros_driver2 CustomMsg to PointCloud2 for RViz",
    license="MIT",
    entry_points={
        "console_scripts": [
            "livox2_to_pc2 = livox2_to_pc2.livox2_to_pc2_node:main",
        ],
    },
)