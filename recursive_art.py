""" Computational art mini project 2 """
""" This program creates art using computations"""
import random
import math
from PIL import Image


functions = ['prod', 'avg', 'sin_pi', 'cos_pi', 'x', 'y', 'square', 'abs_value']
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

  
    depth = random.randint(min_depth, max_depth) # chooses a random integer for the depth
    func_list0 = ['x', 'y', 't'] #zero input arguments
    func_list1 = ['sin_pi', 'cos_pi', 'square', 'abs_value']
    func_list2 = ['prod', 'avg']
    total_func_list = ['sin_pi', 'cos_pi', 'square', 'abs_value', 'prod', 'avg']
    res = [] # This is an empty list but will later store the random function

    if depth <= 0:
        res.append(random.choice(func_list0))
        return res
    else:
        f = random.choice(total_func_list)
        res.append(f)
        if(f in func_list2):
            res.append(build_random_function(min_depth - 1, max_depth - 1))
            res.append(build_random_function(min_depth - 1, max_depth - 1))
        else: # function only takes one argument 
            res.append(build_random_function(min_depth - 1, max_depth - 1))

        return res



def evaluate_random_function(f, x, y, t):
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
    """
    if len(f) == 1:
        if f == ["x"]:
            return x
        elif f == ["y"]:
            return y
        elif f == ["t"]:
            return t
    if f[0] == 'prod': # prod(a,b) = ab
        return float(evaluate_random_function(f[1], x, y, t)) * \
        float(evaluate_random_function(f[2], x, y, t))
    elif f[0] == 'avg': # avg(a,b) = 0.5*(a+b)
        return .5*(evaluate_random_function(f[1], x, y, t)+evaluate_random_function(f[2], x, y, t))
    elif f[0] == 'sin_pi': # sin_pi(a) = sin(pi*a)
        return math.sin(math.pi * evaluate_random_function(f[1], x, y, t))
    elif f[0] == 'cos_pi': # cos_pi(a) = cos(pi*a)
        return math.cos(math.pi * evaluate_random_function(f[1], x, y, t))
    elif f[0] == 'square': # square(a) = a^2
        return (evaluate_random_function(f[1], x, y, t))**2
    elif f[0] == 'abs_value': # abs_value(a) = abs(a)
        return abs(evaluate_random_function(f[1], x, y, t))
    elif f[0] == 'x': # x(a,b,c) = a
        return x
    elif f[0] == 'y': # y(a,b,c) = b
        return y
    elif f[0] == 't': # y(a,b,c) = c
        return t


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
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
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    val = float(val)
    input_interval_start = float(input_interval_start)
    input_interval_end = float(input_interval_end)
    output_interval_start = float(output_interval_start)
    output_inteval_end = float(output_interval_end)

    slope = (output_interval_end - output_interval_start) / (input_interval_end - input_interval_start)
    outputValue = (slope * (val - input_interval_start)) + output_interval_start
    return outputValue



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
    return int(remap_interval(val, -1, 1, 0, 255))


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
    # red_function = ["x"]
    # green_function = ["y"]
    # blue_function = ["x"]
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y, t)),
                    color_map(evaluate_random_function(green_function, x, y, t)),
                    color_map(evaluate_random_function(blue_function, x, y, t))
                    )
    im.save(filename)




def movie_frames(t_begining, t_end, x_size=350, y_size=350):
    '''This makes the frames of the movie from a red function, green function and blue function. 
        begining = first frame, 
        end = last frame
    '''
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)
    t_size = t_end - t_begining
    # Create image and loop over all pixels
    list_of_pixels = []
    for t in range(t_size):
        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        filename = '{}{}{}'.format('frame',t,'.png')
        t = remap_interval(t, 0, t_size,-1, 1)
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                
                pixels[i, j] = (
                        color_map(evaluate_random_function(red_function, x, y, t)),
                        color_map(evaluate_random_function(green_function, x, y, t)),
                        color_map(evaluate_random_function(blue_function, x, y, t))
                        )
        list_of_pixels.append(pixels)
        # print color_map(evaluate_random_function(red_function, 100, 100, t)) # This was used for testing when my frames were all the same
        im.save(filename)






if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # Create some computational art!
    #generate_art("example70.png")
    movie_frames(1, 40)
