# set -x

cd ../..
echo "Script executed from: ${PWD}"

#!/bin/bash
if [ ! -d build ]; then
    # If it doesn't exist, create it
    mkdir build
fi

# Change into the build directory
cd build

# Clean up the build directory by removing its contents safely
rm -rf *

# # Running CMake and Make
cmake -DCMAKE_TOOLCHAIN_FILE=~/vcpkg/scripts/buildsystems/vcpkg.cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DBENCHMARK_OPTIMIZED=OFF -DTIME_LOG_OPEN=ON ..
make -j12

cd ../test/scripts
echo "Script executed from: ${PWD}"
# run executable
python3 run.py /home/dc/dASH_Xplorer/downloads/slam_test/ ../../build/Release/dashXplorer/dpack_test ../path.json 2 /home/dc/dASH_Xplorer/downloads/slam_test/Performance/original

cd ../../build
cmake -DCMAKE_TOOLCHAIN_FILE=~/vcpkg/scripts/buildsystems/vcpkg.cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DBENCHMARK_OPTIMIZED=ON -DTIME_LOG_OPEN=ON ..
make -j12

cd ../test/scripts
python3 run.py /home/dc/dASH_Xplorer/downloads/slam_test/ ../../build/Release/dashXplorer/dpack_test ../path.json 2 /home/dc/dASH_Xplorer/downloads/slam_test/Performance/optimized

# run read log
python3 read_log.py /home/dc/dASH_Xplorer/downloads/slam_test

