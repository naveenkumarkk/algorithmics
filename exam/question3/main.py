import pathlib
import json
import os
import math
import random
import numpy as np
import cv2
from tqdm import tqdm
from scipy.spatial import cKDTree as KDTree


def get_average_color(img):

    if img.size == 0:
        return (0, 0, 0)
    average_color = np.mean(img, axis=(0, 1))
    if np.isnan(average_color).any():
       
        print("Warning: NaN detected in average color computation.")
        return (0, 0, 0)
    return tuple(int(round(c)) for c in average_color)


CACHE_FILE = "cache.json"

if not os.path.exists(CACHE_FILE):
    imgs_dir = pathlib.Path("animals")
    images = list(imgs_dir.glob("**/*.jpg"))

    data = {}
    for img_path in tqdm(images, desc="Caching Images"):
        img = cv2.imread(str(img_path))
        average_color = get_average_color(img)
        avg_col_key = str(tuple(average_color))
        data.setdefault(avg_col_key, []).append(str(img_path))

    with open(CACHE_FILE, "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)
    print("Caching done.")
else:
    with open(CACHE_FILE, "r") as file:
        data = json.load(file)


color_keys = []
color_values = []
for c_str in data.keys():
    c_tuple = eval(c_str)  
    color_keys.append(c_tuple)
    color_values.append(c_str)

color_array = np.array(color_keys, dtype=np.float32) 
tree = KDTree(color_array)

def get_closest_color_kdtree(color):
    dist, idx = tree.query(np.array(color, dtype=np.float32), k=1)
    return eval(color_values[idx])


resized_tile_cache = {}  

def load_and_resize_tile(path, tw, th):
    key = (path, tw, th)
    if key in resized_tile_cache:
        return resized_tile_cache[key]

    tile_img = cv2.imread(path)
    if tile_img is None:
        return None
    tile_img = cv2.resize(tile_img, (tw, th))
    resized_tile_cache[key] = tile_img
    return tile_img

img = cv2.imread("image.jpg")
if img is None:
    raise FileNotFoundError("image.jpg not found or not readable.")
img_height, img_width, _ = img.shape

tile_height, tile_width = 20, 20
num_tiles_h = img_height // tile_height
num_tiles_w = img_width // tile_width


img = img[: tile_height * num_tiles_h, : tile_width * num_tiles_w]

tiles = []
for y in range(0, img.shape[0], tile_height):
    for x in range(0, img.shape[1], tile_width):
        tiles.append((y, y + tile_height, x, x + tile_width))

print("Creating Mosaic...")
for (y0, y1, x0, x1) in tqdm(tiles, desc="Processing Tiles"):
    tile_region = img[y0:y1, x0:x1]
    if tile_region.size == 0:
        continue

    average_color = get_average_color(tile_region)
    closest_color = get_closest_color_kdtree(average_color)
    paths_for_color = data[str(closest_color)] 
    i_path = random.choice(paths_for_color)

    tile_img = load_and_resize_tile(i_path, tile_width, tile_height)
    if tile_img is None:
        print(f"Warning: Unable to read or resize {i_path}. Skipping.")
        continue
    img[y0:y1, x0:x1] = tile_img

cv2.imwrite("output_mosaic.jpg", img)
print("Mosaic saved to output_mosaic.jpg.")
