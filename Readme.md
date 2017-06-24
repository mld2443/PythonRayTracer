# Python Ray Tracer
![Python 3.5.2](https://img.shields.io/badge/Python-3.5.2-brightgreen.svg)
An adaptation of my earlier Swift 2.3 Ray tracer in the Python language for use with the Texas A&M University class CSCE 435.

## About Ray Tracing
[Ray Tracing](https://en.wikipedia.org/wiki/Ray_tracing_(graphics)) is the name for a complex and thorough image synthesis process. Ray tracing generally involves many complex calculations and approximations of the way light behaves in a system. Often a single pixel is the result of hundreds of samples, each of which recurse and propagate multiple times, making the result look accurate. This accuracy comes with a very high price, long calculations. Because of this, it's generally favorable to build implementations in languages that can optimize for speed. Python is not one of those languages, but it is a very capable language, and the parameters of the scene we'll be tracing will be relatively simple.

## Instructions
The ray tracer should work without any changes, but its single-threaded performance will be very slow.

### Running a sample on the TAMU Supercomputer
This project is designed for use with Python 3. The Supercomputer requires you first set up the environment before running.

1. `module load Python/3.5.2-intel-2017A`
  * this is case sensitive
2. navigate to your preferred working directory and clone: `git clone https://github.com/mld2443/PythonRayTracer`
3. `cd PythonRayTracer`
4. `./Tracer.py --resolution 320x240 --samples 10 --depth 4 --seed 0`
  * `./Tracer.py -h` will tell you about the available arguments
