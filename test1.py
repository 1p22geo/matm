import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import uuid
import os
import json

run_id = uuid.uuid4()
os.mkdir(f"./temp/{run_id}")
os.mkdir(f"./temp/{run_id}/parts")
print(f"\tSTARTING SCRIPT\n\nID: {run_id}\n\n\n")

AVG_EMPTY_ROW = 253.0  # gonna autodetect that later
# average grayscale value in an empty row

img = cv.imread("pages/m_62.png")

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


averages = [row.sum() / row.shape[0] for row in gray]

parts = []

for rn in range(len(gray)):
    if averages[rn] == AVG_EMPTY_ROW:
        continue
    if averages[rn-1] == AVG_EMPTY_ROW:
        # this is the first row after a split
        parts.append([])
    parts[-1].append(gray[rn])


for part in range(len(parts)):
    cv.imwrite(f"./temp/{run_id}/parts/part_{part}.png", np.array(parts[part]))
    print(f"SAVED PART {part} to ./temp/{run_id}/parts/part_{part}.png")


os.system(
    f"texify --max 100\
        --json_path ./temp/{run_id}/texify.json \
        --katex_compatible \
        ./temp/{run_id}/parts/"
)
