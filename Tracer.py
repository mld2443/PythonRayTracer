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
    parser.add_option("-o", "--output", metavar="FILENAME",
                      help="Specify the name of the output file.")

    camera_options = OptionGroup(parser, "Camera Options")
    camera_options.add_option("-r", "--resolution",
                              type="int", nargs=2, metavar="WIDTH HEIGHT",
                              default=(320,240), help="Resolution of output image.")
    camera_options.add_option("-s", "--samples",
                              type="int", default=20,
                              help="How many samples are averaged for a single pixel.")
    camera_options.add_option("-d", "--depth",
                              type="int", default=4,
                              help="How many times a sample ray can bounce or refract.")
    camera_options.add_option("--fov", type="float")

    parser.add_option_group(camera_options)

    scene_options = OptionGroup(parser, "Scene Options")
    scene_options.add_option("-p", "--prepared", action="store_true", default=False,
                             help="If set, draws a scene that is defined in 'Scene.py'.")
    scene_options.add_option("-S", "--seed", type="int",
                             help="If generating a scene, defines the seed of the randomly generated scene. If none is provided, current date is used.")
    scene_options.add_option("-n", "--num-spheres", type="int", default=3,
                             help="If generating a scene, use this option to specify how many spheres to generate.")

    parser.add_option_group(scene_options)

    # Populate the options values
    options, args = parser.parse_args()

    # Make sure there were no extra arguments
    if len(args) != 0:
        parser.error("Too many arguments")

    if options.output:
        filename = options.output
    else:
        # Make a default name if one was not provided
        filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S {}.png".format("p" if options.prepared else options.seed))
    path = os.path.join(os.getcwd(), filename)

    try:
        # Attempt to open the file
        file = open(path, 'wb')
    except FileNotFoundError:
        parser.error("Unable to open file {}".format(args[0]))
    except IsADirectoryError:
        parser.error('Provided path, "{}", is not a file.'.format(args[0]))

    # The parser has served its purpose
    parser.destroy()

    # Drawing the image
    image = Scene.build_and_draw(options)

    # Save the image as a png
    #TODO: Handle other file formats
    image.save(file, "PNG")
    file.close()

if __name__ == "__main__":
    main()
