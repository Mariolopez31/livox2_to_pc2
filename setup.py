from setuptools import setup
import platform
import warnings

package_name = "livox2_to_pc2"

is_raspberry = platform.machine() in ("armv7l", "aarch64")

if is_raspberry:
    warnings.warn(
        f"Package '{package_name}' will NOT be installed because a Raspberry/ARM "
        f"architecture was detected (platform.machine()='{platform.machine()}')."
    )

    setup(
        name=package_name,
        version="0.0.1",
        packages=[],
        data_files=[
            ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
            ("share/" + package_name, ["package.xml"]),
        ],
        install_requires=["setuptools"],
        zip_safe=True,
        maintainer="mario-cirtesu",
        maintainer_email="mario@todo.com",
        description="Skipped on Raspberry/ARM",
        license="MIT",
        entry_points={},
    )
else:
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
