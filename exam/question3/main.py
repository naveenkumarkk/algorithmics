import pathlib
import json
import os
import math
import random
import numpy as np
import cv2
from tqdm import tqdm


def get_average_color(img):
    average_color = np.mean(img, axis=(0, 1))
    return tuple(int(round(c)) for c in average_color)


def get_closest_color(color, colors):
    cr, cg, cb = color
    min_difference = float("inf")
    closest_color = None
    for c in colors:
        r, g, b = eval(c)
        difference = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
        if difference < min_difference:
            min_difference = difference
            closest_color = eval(c)
    return closest_color


if "cache.json" not in os.listdir():
    imgs_dir = pathlib.Path("animals")
    images = list(imgs_dir.glob("**/*.jpg"))

    data = {}
    for img_path in tqdm(images, desc="Caching Images"):
        img = cv2.imread(str(img_path))
        average_color = get_average_color(img)
        if str(tuple(average_color)) in data:
            data[str(tuple(average_color))].append(str(img_path))
        else:
            data[str(tuple(average_color))] = [str(img_path)]
    with open("cache.json", "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)
    print("Caching done")

with open("cache.json", "r") as file:
    data = json.load(file)

# Load the input image
img = cv2.imread('image.jpg')
img_height, img_width, _ = img.shape

# Tile dimensions
tile_height, tile_width = 20, 20
num_tiles_h, num_tiles_w = img_height // tile_height, img_width // tile_width
img = img[:tile_height * num_tiles_h, :tile_width * num_tiles_w]

# Create mosaic
tiles = []
for y in range(0, img_height, tile_height):
    for x in range(0, img_width, tile_width):
        tiles.append((y, y + tile_height, x, x + tile_width))

print("Creating Mosaic...")
for tile in tqdm(tiles, desc="Processing Tiles"):
    y0, y1, x0, x1 = tile
    average_color = get_average_color(img[y0:y1, x0:x1])
    closest_color = get_closest_color(average_color, data.keys())

    # Attempt to load a replacement tile
    i_path = random.choice(data[str(closest_color)])
    i = cv2.imread(i_path)
    if i is None:
        print(f"Warning: Unable to read the image at {i_path}. Skipping this tile.")
        continue
    
    # Resize and replace the tile
    try:
        i = cv2.resize(i, (tile_width, tile_height))
        img[y0:y1, x0:x1] = i
    except Exception as e:
        print(f"Error resizing image {i_path}: {e}")
        continue
