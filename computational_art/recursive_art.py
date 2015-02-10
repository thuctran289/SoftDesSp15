""" TODO: Put your header comment here """

import random
import math
from PIL import Image

operator_table = ["x",
                  "y",
                  "sin_pi",
                  "cos_pi",
                  "prod",
                  "avg"
                  ]

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    # TODO: implement this
    f = []
    #includes depth one operators "x" and "y"
    if min_depth == 1:
        lower_operator_choice  = 0
    else:
        lower_operator_choice  = 2
    #only includes depth one operators "x" and "y". No sin, no cosin, no etc.
    if max_depth ==1:
        upper_operator_choice = 2
    else: 
        upper_operator_choice = 5
    operator = random.randrange(lower_operator_choice,upper_operator_choice)
    f.append(operator_table[operator])
    new_min_depth = min_depth
    if min_depth != 1:
        new_min_depth = min_depth-1
    
    if operator<2:
        pass
    elif operator<4:
        f.append(build_random_function(new_min_depth,max_depth-1))
    else:
        f.append(build_random_function(new_min_depth,max_depth-1))
        f.append(build_random_function(new_min_depth,max_depth-1))

        
    return f

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["prod"],1,2)
        2
        >>> evaluate_random_function(["avg"],1,2)
        1.5
        >>> evaluate_random_function(["cos_pi",["x"]],1,1)
        -1.0
        >>> evaluate_random_function(["sin_pi",["x"]],.5,1)
        1.0
        >>> evaluate_random_function(["prod",["cos_pi",["x"]], ["sin_pi",["y"]]], 0,.5)
        1.0
        >>> evaluate_random_function(["sin_pi",["cos_pi",["x"]]],.25,1)
        0.7956932015674809
    """

    if len(f) == 1:
        if f[0] == "x":
            return x
        elif f[0] == "y":
            return y
        elif f[0] == "prod":
            return x*y
        elif f[0] == "avg":
            return (x+y)/2.
    elif len(f) ==2:
        if f[0] == "sin_pi":
            return math.sin(math.pi*evaluate_random_function(f[1],x,y))
        elif f[0] == "cos_pi":
            return math.cos(math.pi*evaluate_random_function(f[1],x,y))
    else:
        if f[0] == "prod":
            return evaluate_random_function(f[1],x,y)*evaluate_random_function(f[2],x,y)
        elif f[0] == "avg":
            return (evaluate_random_function(f[1],x,y) + evaluate_random_function(f[2],x,y))/2.0

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_interval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    #Gives channel length of output
    new_channel_length = output_interval_end - output_interval_start
    #Input Channel Length
    channel_length = input_interval_end - input_interval_start
    #Subtracts out the initial start to give depth into the channel for the input, and divides by the channel depth. 
    #Essentially gives the ratio of the depth into the channel
    ratio = (val-input_interval_start)/(channel_length + 0.0)
    #Multiplies to find depth into new channel, and adds the starting offset.
    return ratio*new_channel_length + output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    for x in range(0,100):
        title = "myart"+str(x)+".png"
        generate_art(title)
    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
