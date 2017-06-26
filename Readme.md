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
2. `module load myPython/3.5.2-intel-2017A`
  * If this is your first time ever loading this myPython module, please also execute the following:
    1. `$MYCREATEVIRTENV`
    2. `$MYACTIVATE`
    3. `pip install Pillow`
      * Pip may complain that it's not up to date. This shouldn't be a problem.
    4. `$MYDEACTIVATE`
  * After doing the above, your environment is saved, and your `$PYTHONPATH` should now be set. This will be remembered the next time you load the same `myPython` module.
    * To check any of these `$` variables, type `echo` before them to see what they are.
  * If you have any trouble with the Python virtual environments, [please see the HPRC wiki page](https://hprc.tamu.edu/wiki/index.php/SW:Python#User_installed_using_virtual_environments).
3. navigate to your preferred working directory and clone: `git clone https://github.com/mld2443/PythonRayTracer`
4. `cd PythonRayTracer`
5. `./Tracer.py --resolution 320 240 --samples 5 --depth 4`
  * `./Tracer.py -h` will tell you about the available options

## Crash course on why ray tracing is so slow
Without having to read the code, here's where all the time goes. The ray tracer will set up the scene, then it will begin to cast rays. for each pixel, it casts the number of rays specified by `samples` (default 10) with small random offsets to prevent aliasing. Each cast ray then checks every object in the scene for an intersection, and then picks the nearest one. It then either reflects or refracts, casting another ray. This ray casting is recusive and can happen up to `depth` (default 5) times unless the ray does not hit anything.

### Put in perspective
With the default arguments, and the predetermined scene, this is 240 * 144 * 10 = 345,600 samples, each with between 1 to 5 castings. A run with the `--verbose` flag tells me that the program calculated 958,687 rays. Each ray involved calculating the intersection point with every object in the scene (4 quadrics and 1 plane), and then finding the closest. it then calculates the normal, and the bounce, which is different for each material.

Those several million calculations took that same run 150.59s or just shy of 3 minutes. Relatively speaking... that's *very* slow. Most CPUs today can do billions of calculations per second, on one thread. A powerful GPU in a modern video game can blow that out of the water.

#### Okay, but why?
3 Main reasons:
* Python is interpreted.
* This code is single-threaded.
* Ray tracing techniques are *VERY* expensive compared to modern rasterization techniques (depth buffering).
  * Those very techniques are responsible for how easy it would be to implement new features, and how good they look.
There are two more reasons why it's slower: this code makes very little use of [localities](https://en.wikipedia.org/wiki/Locality_of_reference) , (which is something a compiler might help with), and I've opted for a recursive approach for the actual tracing, (as opposed to an iterative one).

#### Can it go faster?
Absolutely. There are at least 3 fundamentally different ways I can think of to multi-thread the application. This is actually quite open-ended.
