from pathlib import Path
import subprocess
import os
import shutil


def build_cmake():
    # Create build directory
    build_dir = os.path.join(os.getcwd(), 'build')
    os.makedirs(build_dir, exist_ok=True)
    os.chdir(build_dir)
    
    # Set the target dir for cmake to install to
    target_dir = Path(__file__).parent / 'pyorbbecsdk' / 'bindings'
    # Delete the target dir if it exists
    if target_dir.exists():
        shutil.rmtree(target_dir)
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy the .pyi stub files to the target dir
    stub_file = Path(__file__).parent / 'stubs' / 'pyorbbecsdk.pyi'
    target_file = target_dir / 'pyorbbecsdk.pyi'
    shutil.copy(stub_file, target_file)
        
    # Run CMake
    pybind11_dir = subprocess.check_output(
        ['poetry', 'run', 'python', '-c', 'import pybind11; print(pybind11.get_cmake_dir())'],
        universal_newlines=True
    ).strip()

    cmake_args = [
        '-Dpybind11_DIR={}'.format(pybind11_dir),
        '..'
    ]
    subprocess.check_call(['cmake'] + cmake_args)
    subprocess.check_call(['make', '-j4'])
    subprocess.check_call(['make', 'install'])

if __name__ == "__main__":
    build_cmake()
