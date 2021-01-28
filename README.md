# Vineyard World Creator

Quickly create world files with simulated vineyards.

![Example Vineyard](https://user-images.githubusercontent.com/35245591/106079722-c0989580-60e3-11eb-99f1-97d4fbfb0f54.png)

## Info

This module was created for use with the [Warthog_Velodyne module](https://github.com/aaronzberger/CMU_Warthog_Velodyne). 

The Vine models that are referenced in the world files created by this program can be downloaded via that repo. They are required for these world files to be usable in Gazebo.

Both Python 2.7 and Python 3.6 have been tested and work with this module.

Feel free to edit or redistribute this code.

If you have any questions, or if this module does not work for you, please contact me at azberger@andrew.cmu.edu

## Usage
```
create_world.py [OPTIONS]

optional arguments:
  -h, --help            show this help menu
  --num_rows NUM_ROWS, -n NUM_ROWS
                        number of rows to use. Default: randomize in the range [2:10]
                        
  -widths WIDTHS [WIDTHS ...], -w WIDTHS [WIDTHS ...]
                        list of row widths (floats). Simply list the distances between each row (left to right)
                        
  --row_width ROW_WIDTH [ROW_WIDTH ...], -rw ROW_WIDTH [ROW_WIDTH ...]
                        distance between each row (float) or range in which to randomize (float float) Default: randomize in range [2:5]
                        
  --row_length ROW_LENGTH, -rl ROW_LENGTH
                        length of the rows in meters (just a single value)
                        
  --filename FILENAME, -f FILENAME
                        full path to save the file in
                        
  --noise_pos NOISE_POS, -np NOISE_POS
                        standard deviation of the Gaussian noise to add to the positions of the vines (0.1 is a good place to start)
                        
  --noise_ang NOISE_ANG, -na NOISE_ANG
                        standard deviation of the Gaussian noise to add to the angles of the vines (0.1 is a good place to start)
