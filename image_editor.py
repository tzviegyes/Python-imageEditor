#################################################################
# FILE : image_editor.py
# WRITER : Tzvi Egyes , Tzvi.egyes@mail.huji.ac.il , 212795728
# EXERCISE : intro2cs ex6 2025
# DESCRIPTION: A simple program for editing images
#
# WEB PAGES I USED: https://www.datacamp.com/tutorial/how-to-exit-python-a-quick-tutorial
# NOTES: some of the long functions I didn't devide into smaller functions in order to minimize running
#   time of calling functions with large matixes and returnung them.
#   Imported UnidentifiedImageError from PIL, didn't use the module for anything else
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex6_helper import *
from typing import Optional
from copy import deepcopy
import sys
from PIL import UnidentifiedImageError

##############################################################################
#                                 CONSTANTS                                  #
##############################################################################
RED_AVERAGE = 0.299
GREEN_AVERAGE = 0.587
BLUE_AVERAGE = 0.114
COLOR_SHADES = 256
BLACK = 0
WHITE = 255

INPUT_TOOL_MESSAGE = ("choose from the following tools: \n"
                 "1 - convert to black & white\n"
                 "2 - blure the image\n"
                 "3 - resize picture\n"
                 "4 - turn picture 90 degrees\n"
                 "5 - find edges\n"
                 "6 - quantize image\n"
                 "7 - show image\n"
                 "8 - exit program\n")
INPUT_ROTATE = "what direction? enter R or L\n"
INPUT_NEW_SIZE = "input size of new image: new_hight,new_width\n"
INPUT_QUANTIZE = "input N intager\n"
INPUT_KERNAL_SIZE = "input kernal size. odd positive integer\n"
INPUT_EDGES = "input blur, block, constant: 3 integers seperated with commas all non-negitve, blur and block are odd\n"
INPUT_PATH_TO_SAVE = "input path of where to save picture\n"
ERROR_INVALID_INPUT = "your input is invalid"
TOOL_NUMBERS = "12345678"
MINIMUM_SIZE_FOR_RESIZE = 2



##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    """seperates image with any number of chanels to singal-chanel images"""
    rows = len(image)
    columns = len(image[0])
    chanels = len(image[0][0])

    seperated_image = []
    for chanel in range(chanels):
        singal_chanel = []
        for row in range(rows):
            singal_row = []
            for column in range(columns):
                singal_row.append(image[row][column][chanel])
            singal_chanel.append(singal_row)
        seperated_image.append(singal_chanel)
    return seperated_image


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    """combines singal-chanel images  to multi-chanel image"""
    rows = len(channels[0])
    columns = len(channels[0][0])
    chanels = len(channels)

    combined_image = []
    for row in range(rows):
        singal_row = []
        for column in range(columns):
            cell = []
            for chanel in range(chanels):
                cell.append(channels[chanel][row][column])
            singal_row.append(cell)
        combined_image.append(singal_row)
    return combined_image


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """converts 3dimentional colured image to 2dimentional gray_scale image"""
    rows = len(colored_image)
    columns = len(colored_image[0])
    gray_scale = []
    for row in range(rows):
        singal_row = []
        for column in range(columns):
            pixel = colored_image[row][column]
            singal_row.append((pixel[0] * RED_AVERAGE + pixel[1] * GREEN_AVERAGE + pixel[2] * BLUE_AVERAGE).__round__())
        gray_scale.append(singal_row)
    return gray_scale


def blur_kernel(size: int) -> Kernel:
    """returns kernal: sixe*sixe list of 1/size^2"""
    return [[(1/size ** 2) for i in range(size)] for j in range(size)]


def color_in_range(num: float) -> int:
    """returns 0 for negetive numbers, 255 for larger numbers.
    if in range returns the number rounded to clossest integer"""
    if num < 0:
        return 0
    elif num > 255:
        return 255
    else:
        return num.__round__()


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    """blurs image using input kernel.
    for each pixel looks in the pixel serounding and multiplies by the valure of corresponding kernel cell"""
    kernal_size = len(kernel)
    half_kernal_size = int((kernal_size - 1) / 2)
    image_rows = len(image)
    image_columns = len(image[0])
    blured_image = []
    # iterate over all image pixals
    for row in range(image_rows):
        blured_row = []
        for column in range(image_columns):
            cell = 0

            # iterate over kernal cells
            for kernal_row in range(kernal_size):
                for kernal_column in range(kernal_size):
                    kenal_image_row = row + (kernal_row - half_kernal_size)
                    kenal_image_column = column + (kernal_column - half_kernal_size)
                    # check if the coresponding pixel is in the picture
                    if 0 <= kenal_image_row < image_rows and 0 <= kenal_image_column < image_columns:
                        coresponding_cell = image[kenal_image_row][kenal_image_column]
                    else: # if the coresponding pixel is not in the picture
                        coresponding_cell = image[row][column]
                    cell += (coresponding_cell * kernel[kernal_row][kernal_column])

            blured_row.append(color_in_range(cell))
        blured_image.append(blured_row)
    return blured_image


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    """gets a 2D image and a point in the matrix,
    returns the bilinear_interpolation around the point"""
    # if in botom right corner
    if x >= len(image[0]) - 1 and y >= len(image) - 1:
        a = b = c = d = image[len(image) - 1][len(image[0]) - 1]

    # if on vertical edge
    elif x >= len(image[0]) - 1:
        a = c = image[int(y // 1)][len(image[0]) - 1]
        b = d = image[int(y // 1 + 1)][len(image[0]) - 1]

    # if on horizontal edge
    elif y >= len(image) - 1:
        a = b = image[len(image) - 1][int(x // 1)]
        c = d = image[len(image) - 1][int(x // 1 + 1)]

    # if not on edges -> has 4 surounding pixels
    else:
        a = image[int(y // 1)][int(x // 1)]
        b = image[int(y // 1 + 1)][int(x // 1)]
        c = image[int(y // 1)][int(x // 1 + 1)]
        d = image[int(y // 1 + 1)][int(x // 1 + 1)]
    d_x = x % 1
    d_y = y % 1
    # bilinear formula
    answer = a * (1 - d_x) * (1 -d_y) + b * (1 - d_x) * d_y + c * d_x * (1 - d_y) + d * d_x * d_y
    return answer.__round__()


def point_in_original(original_rows, original_columns, new_rows, new_columns, cell_row, cell_column):
    """returns the point in matrix with the ratio of new size"""
    column = cell_column * (original_columns - 1) / (new_columns - 1)
    row = cell_row * (original_rows - 1) / (new_rows - 1)
    return column, row


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    """changes the size of image to new hight and new width"""
    original_rows = len(image)
    original_columns = len(image[0])
    new_image = []
    for row in range(new_height):
        new_row = []
        for column in range(new_width):
            cell = point_in_original(original_rows, original_columns, new_height, new_width, row, column)
            new_row.append(bilinear_interpolation(image, cell[1], cell[0]))
        new_image.append(new_row)

    return new_image


def rotate_90_right(image):
    """rotates image 90 degrees to the right"""
    rotated = [[image[x][y] for x in range(len(image)-1, -1, -1)]for y in range(len(image[0]))]
    return rotated


def rotate_90(image: Image, direction: str) -> Image:
    """if input right -> turns right
    if left -> turns right three times"""
    if direction == 'R':
        return rotate_90_right(image)
    else: # direction == 'L'
        # 3 turns right is one turn left
        return rotate_90_right(rotate_90_right(rotate_90_right(image)))


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    """finds edges of objects in image, blurs, and compares to average of block - c """
    blured_image = apply_kernel(image, blur_kernel(blur_size))
    block_kenal = blur_kernel(block_size)
    threshholded_image = apply_kernel(blured_image,block_kenal)
    for y in range(len(image)):
        for x in range(len(image[0])):
            if threshholded_image[y][x] - c > blured_image[y][x]:
                threshholded_image[y][x] = BLACK
            else:
                threshholded_image[y][x] = WHITE
    return threshholded_image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    """reduces shades in 2D images to given N"""
    quantized_image = deepcopy(image)
    for row in range(len(image)):
        for column in range(len(image[0])):
            quantized_image[row][column] = (((quantized_image[row][column] * N / COLOR_SHADES) // 1) * (COLOR_SHADES - 1) / (N - 1)).__round__()
    return quantized_image


def got_two_arguments():
    """returns True if got right amount of arguments from user"""
    if len(sys.argv) != 2:
        print("wrong number of arguments")
        return False
    return True


def valid_load_image():
    """returns True if the program is able to load the image"""
    try:
        input_image = load_image(sys.argv[1])
    except FileNotFoundError:
        print("File not found")
        return False
    except UnidentifiedImageError:
        print("File not identified")
        return False
    return True

def valid_input_tool(user_input):
    """returns True if the user chose a valid tool number"""
    if not user_input in TOOL_NUMBERS or len(user_input) > 1:
        print(ERROR_INVALID_INPUT)
        return False
    else:
        return True

def is_positive_odd(number: float):
    """returns True if the number given is positive and odd (and whole)"""
    if number != int(number):
        return False
    if number < 1 or number % 2 != 1:
        return False
    return True

def is_grayscale(image):
    """returns True if the image is 2D, if 3D returns False"""
    if type(image[0][0]) == list:
        return False
    else:
        return True

def use_grayscale(image):
    """returns a grayscale image"""
    if is_grayscale(image):
        print("your image is black and White")
        return image
    else:
        return RGB2grayscale(image)

def use_blur(image):
    """asks for relavent input, check the input is valid and returns a blured image"""
    try:
        kernal_size = float(input(INPUT_KERNAL_SIZE))
        if is_positive_odd(kernal_size):
            if is_grayscale(image):
                return apply_kernel(image, blur_kernel(int(kernal_size)))
            else:
                seperated = separate_channels(image)
                seperated_blured = [apply_kernel(seperated[color], blur_kernel(int(kernal_size))) for color in range(len(seperated))]
                return combine_channels(seperated_blured)
                
        else:
            print(ERROR_INVALID_INPUT)
            return image
    except ValueError:
        print(ERROR_INVALID_INPUT)
        return image

def use_resize(image):
    """asks for relavent input, check the input is valid and returns a resized image"""
    try:
        size_input = input(INPUT_NEW_SIZE).split(',')
        new_hight = int(size_input[0])
        new_width = int(size_input[1])
        # not integers
        if float(size_input[0]) != new_hight or float(size_input[1]) != new_width:
            print(ERROR_INVALID_INPUT)
            return image

        # numbers too low or not 2 numbers with a comma
        if new_width < MINIMUM_SIZE_FOR_RESIZE or new_hight < MINIMUM_SIZE_FOR_RESIZE or len(size_input) != 2:
            print(ERROR_INVALID_INPUT)
            return image

        if is_grayscale(image):
            return resize(image, new_hight, new_width)
        else:
            """devide to three, resize each and combine"""
            seperated = separate_channels(image)
            seperated_resized = [resize(seperated[color], new_hight, new_width) for color in range(len(seperated))]
            return combine_channels(seperated_resized)

    # didnt get numbers
    except ValueError:
        print(ERROR_INVALID_INPUT)
        return image
    # didnt get enough arguments
    except IndexError:
        print(ERROR_INVALID_INPUT)
        return image

def use_rotate(image):
    """asks for relavent input, check the input is valid and returns a rotated image"""
    rotate_direction = input(INPUT_ROTATE)
    if rotate_direction != 'L' and rotate_direction != 'R':
        print(ERROR_INVALID_INPUT)
        return image
    else:
        return rotate_90(image, rotate_direction)

def use_get_edges(image):
    """asks for relavent input, check the input is valid and returns an image with the outlines of the objects"""
    try:
        edges_input = input(INPUT_EDGES).split(',')
        input_blur = float(edges_input[0])
        input_block = float(edges_input[1])
        input_c = float(edges_input[2])
        if int(input_c) != input_c or input_c < 0 or len(edges_input) != 3:
            print(ERROR_INVALID_INPUT)
            return image
        if not is_positive_odd(input_blur) or not is_positive_odd(input_block):
            print(ERROR_INVALID_INPUT)
            return image

        # input is valid
        if is_grayscale(image):
            return get_edges(image, int(input_blur), int(input_block), int(input_c))
        else:
            return get_edges(RGB2grayscale(image), int(input_blur), int(input_block), int(input_c))

    # didnt get numbers
    except ValueError:
        print(ERROR_INVALID_INPUT)
        return image
    # didnt get enough arguments
    except IndexError:
        print(ERROR_INVALID_INPUT)
        return image


def use_quantize(image):
    """asks for relavent input, check the input is valid and returns a quantized image"""
    try:
        quantize_input = float(input(INPUT_QUANTIZE))
        if quantize_input < 2 or int(quantize_input) != quantize_input:
            print(ERROR_INVALID_INPUT)
            return image
        else:
            if is_grayscale(image):
                return quantize(image, int(quantize_input))
            else:
                """devide to three, quantize each and combine"""
                seperated = separate_channels(image)
                seperated_resized = [quantize(seperated[color], int(quantize_input)) for color in range(len(seperated))]
                return combine_channels(seperated_resized)

    except ValueError:
        print(ERROR_INVALID_INPUT)
        return image


def use_exit(image):
    """asks for file path, saves the image in the path and exits the program"""
    try:
        path_to_save = input(INPUT_PATH_TO_SAVE)
        save_image(image, path_to_save)
        sys.exit()
    except:
        print(ERROR_INVALID_INPUT)
        sys.exit()


def use_any_tool(image):
    """asks user to pick a tool and calls the function that uses the tool"""
    while True:
        user_input = input(INPUT_TOOL_MESSAGE)
        if valid_input_tool(user_input):
            break

    if user_input == "1":   # grayscale
        return use_grayscale(image)

    if user_input == "2":   # blur
        return use_blur(image)

    if user_input == "3":   # change size
        return use_resize(image)

    if user_input == "4":   # rotate
        return use_rotate(image)

    if user_input == "5":   # edges
        return use_get_edges(image)

    if user_input == "6":   # quantize
        return use_quantize(image)

    if user_input == "7":   # show image
        show_image(image)
        return image

    if user_input == "8":   # exit
        use_exit(image)


if __name__ == '__main__':
    # check that got two arguments and image file is valid
    if not got_two_arguments() or not valid_load_image():
        print(ERROR_INVALID_INPUT)
    else:
        input_image = load_image(sys.argv[1])
        modified_image = use_any_tool(input_image)

        while True:
            copy_of_image = deepcopy(modified_image)
            modified_image = use_any_tool(copy_of_image)
