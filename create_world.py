import argparse
import random
import numpy as np
import math
from get_vine_model import get_vine_model

# Delta X between vine models (this is specific to these models)
vine_step = 1.76

# Gazebo coordinates are offset; everything needs to be shifted left
gazebo_left_offset = 1

# Gather user inputs
parser = argparse.ArgumentParser(description='Gazebo Vineyard World Creator')
parser.add_argument(
    '--num_rows', type=int, default=None,
    help='number of rows to use. Default: randomize in the range [2:10]')
parser.add_argument(
    '-widths', nargs='+', default=None, help='list of row widths (floats).' +
    ' Simply list the distances between each row (left to right)')
parser.add_argument(
    '--row_width', nargs='+', default=None,
    help='distance between each row (float) or range in which to randomize ' +
    '(float float) Default: randomize in range [2:5]')
parser.add_argument(
    '--row_length', type=float, default=20,
    help='length of the rows in meters (just a single value)')
parser.add_argument(
    '--filename', type=str, default='output.world',
    help='full path to save the file in')
parser.add_argument(
    '--noise_pos', type=float, default=0.0,
    help='standard deviation of the Gaussian noise to add to the positions ' +
    'of the vines (0.1 is a good place to start)')
parser.add_argument(
    '--noise_ang', type=float, default=0.0,
    help='standard deviation of the Gaussian noise to add to the angles ' +
    'of the vines (0.1 is a good place to start)')

args = parser.parse_args()
if args.widths is not None:
    # Argparse reads strings, so we need to convert to float
    args.widths = [float(i) for i in args.widths]
    if args.num_rows is not None or args.row_width is not None:
        raise ValueError(
            'If you input -widths argument, you cannot input --num_rows or ' +
            '--row_width arguments, since they might contradict.')
    args.num_rows = len(args.widths) + 1
else:
    if args.num_rows is None:
        # Default specified in argparse
        args.num_rows = int(random.random() * 8) + 2
    if args.row_width is None:
        # Default specified in argparse
        args.row_width = [2.0, 5.0]
    # Individual row widths were not given, so we now generate those values
    if not len(args.row_width) == 1 or len(args.row_width) == 2:
        raise ValueError('--row_width argument must be either 1 or 2 integers')
    if len(args.row_width) == 2:
        args.widths = np.random.uniform(
            low=float(args.row_width[0]), high=float(args.row_width[1]),
            size=args.num_rows)
        print('Row widths have been randomized to {}'.format(args.widths))
    else:
        args.widths = [float(args.row_width[0])] * args.num_rows

# We'll hold on to the string sections until we have collected all of them,
# since we need to put all the first parts, then all the second parts
first_parts = []
second_parts = []

# Keep track of how many of each vine we use, for printing at the end
vine_types = [0, 0, 0, 0]


def make_row(y_pos, length, index):
    '''
    Generate the string sections for all of the vines in a row

    Parameters:
        y_pos (float): the y position of the row
        length (float): the length of the row
        index (int): the index of the row (to use in naming vines)
    '''
    for vine_num, x_pos in enumerate(
            np.arange(-args.row_length / 2, args.row_length / 2, vine_step)):
        name = '{}_{}'.format(index, vine_num + 1)
        vine_type = int(random.random() * 3 + 1)
        vine_types[vine_type] += 1
        y_noise = np.random.normal(
            loc=0, scale=args.noise_pos) if args.noise_pos else 0
        ang_noise = np.random.normal(
            loc=0, scale=args.noise_ang) if args.noise_ang else 0
        first_part, second_part = get_vine_model(
            name=name, vine_type=vine_type, x=x_pos,
            y=y_pos - gazebo_left_offset + y_noise, z=0,
            theta=math.pi / 2 + ang_noise)
        first_parts.append(first_part)
        second_parts.append(second_part)


# Generate all the rows
y_pos = -(sum(args.widths) / 2)
make_row(y_pos=y_pos, length=args.row_length, index=1)
for row_num, width in enumerate(args.widths):
    y_pos += width
    make_row(y_pos=y_pos, length=args.row_length, index=row_num + 2)

# Open the text files needed for the output file
before_vine_models_text = open('before_vine_models.txt', 'r')
after_vine_models_text = open('after_vine_models.txt', 'r')
end_text = open('end.txt', 'r')

output_file = open(args.filename, 'w')

# Write the text needed before the first part strings
output_file.write(before_vine_models_text.read())
before_vine_models_text.close()

# Write the first part strings
for model in first_parts:
    output_file.write(model)

# Write the text needed between the first and second part strings
output_file.write(after_vine_models_text.read())
after_vine_models_text.close()

# Write the second part strings
for model in second_parts:
    output_file.write(model)

# Write the text needed at the end
output_file.write(end_text.read())
end_text.close()
output_file.close()

print('''
Created a vineyard at {}

containing {} rows, which each contain {} vine models.

Which vine model is random, but this vineyard uses:
  {} Vine1
  {} Vine2
  {} Vine3
'''.format(args.filename, args.num_rows,
           int(math.ceil(args.row_length / vine_step)),
           vine_types[1], vine_types[2], vine_types[3]))
