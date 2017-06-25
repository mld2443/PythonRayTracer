#!/usr/bin/env python3

from optparse import OptionParser, OptionGroup
from datetime import datetime
import os
import Scene

def main():
    # Define all the options for the ray tracing environment
    parser = OptionParser(version="1.0")

    parser.add_option("-v", "--verbose", action="store_true", default=False,
                      help="Flag for output of detailed render and timing information.")
    parser.add_option("--debug", action="store_true", default=False,
                      help="Flag for the printing of debug info.")
    parser.add_option("-o", "--output", metavar="FILENAME",
                      help="Specify the name of the output file.")
    parser.add_option("-m", "--multi", metavar="THREADS", type="int", default=1,
                      help="Number of threads to use while rendering. Default: 1.")

    cam_opts = OptionGroup(parser, "Camera Options")
    cam_opts.add_option("-r", "--resolution", type="int", nargs=2,
                        metavar="WIDTH HEIGHT", default=(320,240),
                        help="Resolution of output image.")
    cam_opts.add_option("--fov", type="float", default=95.0,
                        help="The horizontal field of view of the capture.")
    cam_opts.add_option("-s", "--samples", type="int", default=20,
                        help="How many samples are averaged for a single pixel.")
    cam_opts.add_option("-d", "--depth", type="int", default=4,
                        help="How many times a sample ray can bounce or refract.")

    parser.add_option_group(cam_opts)

    scn_opts = OptionGroup(parser, "Scene Options")
    scn_opts.add_option("-p", "--prepared", action="store_true", default=False,
                        help="If set, draws the scene that is defined in 'Scene.py'.")
    scn_opts.add_option("-S", "--seed", type="int",
                        help="If generating a scene, defines the seed of the randomly generated scene. If none is provided, current date is used.")
    scn_opts.add_option("-n", "--num-spheres", type="int", default=3,
                        help="If generating a scene, use this option to specify how many spheres to generate.")

    parser.add_option_group(scn_opts)

    # Populate the options values
    params, args = parser.parse_args()

    # Make sure there were no extra arguments
    if len(args) != 0:
        parser.error("Too many arguments")

    if params.output is None:
        # Make a default name if one was not provided
        setattr(params,"output",datetime.now().strftime("%Y-%m-%d %H.%M.%S.png"))
    path = os.path.join(os.getcwd(), params.output)

    try:
        # Attempt to open the file
        file = open(path, 'wb')
    except FileNotFoundError:
        parser.error("Unable to open file {}".format(params.output))
    except IsADirectoryError:
        parser.error("Provided path, '{}', is not a file.".format(params.output))

    # The parser has served its purpose
    parser.destroy()

    # Drawing the image
    image = Scene.build_and_draw(params)

    # Save the image as a png
    #TODO: Handle other file formats
    image.save(file, "PNG")
    file.close()

if __name__ == "__main__":
    main()
