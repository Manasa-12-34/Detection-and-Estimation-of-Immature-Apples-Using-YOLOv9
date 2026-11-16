import os
import cv2
import numpy as np

# ==========================
# YOLO LABEL FILE
# ==========================
label_folder = input("Enter labels folder path: ").strip()

txt_files = [f for f in os.listdir(label_folder) if f.endswith(".txt")]

if not txt_files:
    print("No detection results found!")
    exit()

label_file = os.path.join(label_folder, txt_files[0])

# ==========================
# APPLE COUNT + SIZE
# ==========================

small = 0
medium = 0
large = 0

with open(label_file, "r") as f:
    lines = f.readlines()

    apple_count = len(lines)

    for line in lines:
        parts = line.strip().split()

        # YOLO format:
        # class x_center y_center width height

        w = float(parts[3])
        h = float(parts[4])

        area = w * h

        if area < 0.02:
            small += 1
        elif area < 0.08:
            medium += 1
        else:
            large += 1

# ==========================
# YIELD ESTIMATION
# ==========================

avg_weight = 150  # grams per apple
yield_kg = (apple_count * avg_weight) / 1000

# ==========================
# RIPENESS ANALYSIS
# ==========================

image_path = input("Enter image path: ").strip()

img = cv2.imread(image_path)

if img is None:
    print("Image not found!")
    exit()

b, g, r = cv2.split(img)

red_pixels = np.sum((r > g) & (r > b))
green_pixels = np.sum((g > r) & (g > b))

total_pixels = red_pixels + green_pixels

if total_pixels == 0:
    green_pct = 0
    red_pct = 0
    ripeness = "Unknown"
else:
    green_pct = (green_pixels / total_pixels) * 100
    red_pct = (red_pixels / total_pixels) * 100

    if green_pixels > red_pixels:
        ripeness = "Mostly Unripe"
    elif red_pixels > green_pixels:
        ripeness = "Mostly Ripe"
    else:
        ripeness = "Mixed"

# ==========================
# FINAL REPORT
# ==========================

print("\n===== APPLE ANALYSIS REPORT =====")

print(f"Apples Detected : {apple_count}")

print("\nSize Estimation")
print(f"Small Apples  : {small}")
print(f"Medium Apples : {medium}")
print(f"Large Apples  : {large}")

print(f"\nEstimated Yield : {yield_kg:.2f} kg")

print(f"\nGreen Percentage : {green_pct:.2f}%")
print(f"Red Percentage  : {red_pct:.2f}%")

print(f"\nRipeness Status : {ripeness}")