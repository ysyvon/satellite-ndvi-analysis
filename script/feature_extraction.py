import tkinter as tk
from tkinter import filedialog
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
import os
from datetime import datetime
from rasterio.transform import from_origin
import rasterio.features

# Function to read Red and NIR bands and calculate NDVI
def calculate_ndvi(red_band_path, nir_band_path):
    with rasterio.open(red_band_path) as red_src:
        red_band = red_src.read(1)  # Read the first band
        red_nodata = red_src.nodata  # Get NoData value for the Red band
        print(f"Red band NoData value: {red_nodata}")
        print(f"Red band min: {np.min(red_band)}, max: {np.max(red_band)}")

    with rasterio.open(nir_band_path) as nir_src:
        nir_band = nir_src.read(1)  # Read the first band
        nir_nodata = nir_src.nodata  # Get NoData value for the NIR band
        print(f"NIR band NoData value: {nir_nodata}")
        print(f"NIR band min: {np.min(nir_band)}, max: {np.max(nir_band)}")

    # Apply scaling for Landsat 8 (divide by 10000 to normalize reflectance values)
    red_band = red_band / 10000.0  # Scaling for Landsat reflectance
    nir_band = nir_band / 10000.0  # Scaling for Landsat reflectance

    # Mask NoData values in both bands if they exist
    if red_nodata is not None:
        red_band = np.ma.masked_equal(red_band, red_nodata)
    if nir_nodata is not None:
        nir_band = np.ma.masked_equal(nir_band, nir_nodata)

    # Calculate NDVI: (NIR - Red) / (NIR + Red)
    ndvi = (nir_band - red_band) / (nir_band + red_band + 1e-10)

    return ndvi, nir_src

# Function to classify NDVI into vegetation, water, and barren land
def classify_ndvi(ndvi, output_path, crs, transform):
    # Set thresholds for classification
    vegetation = (ndvi > 0.3)
    water = (ndvi < 0.1)
    barren_land = (ndvi >= 0) & (ndvi < 0.3)

    # Create the classified image
    classified_image = np.zeros_like(ndvi, dtype=np.uint8)
    classified_image[vegetation] = 1  # Vegetation = 1
    classified_image[water] = 2       # Water = 2
    classified_image[barren_land] = 3  # Barren land = 3

    # Save the classified image
    with rasterio.open(output_path, 'w', driver='GTiff', count=1, dtype='uint8',
                       width=classified_image.shape[1], height=classified_image.shape[0],
                       crs=crs, transform=transform) as dst:
        dst.write(classified_image, 1)

    print(f"Classification saved to: {output_path}")

    # Visualize the classified image for debugging
    plt.imshow(classified_image, cmap='tab20')  # Use a categorical colormap for classification
    plt.colorbar()  # Show color bar for classification values (1 = Vegetation, 2 = Water, 3 = Barren Land)
    plt.title('Classified NDVI Image')
    plt.show()

    return classified_image

# Function to extract features from the classified image
def extract_features(classified_image, output_folder, crs, transform):
    vegetation_areas = classified_image == 1  # Vegetation is classified as 1

    # Convert the vegetation areas to polygons (GeoDataFrame)
    vegetation_polygons = []
    for shape, value in rasterio.features.shapes(classified_image, mask=vegetation_areas, transform=transform):
        if value == 1:  # Only keep vegetation polygons
            geometry = Polygon(shape['coordinates'][0])
            if geometry.is_valid:  # Check if polygon geometry is valid
                vegetation_polygons.append(geometry)
            else:
                print("Invalid geometry found and skipped.")

    # Create a GeoDataFrame for vegetation polygons
    gdf = gpd.GeoDataFrame({'geometry': vegetation_polygons})
    gdf.crs = crs  # Make sure CRS is assigned correctly (the CRS of the raster)

    # Save the vegetation polygons as a shapefile
    vegetation_shapefile = os.path.join(output_folder, 'vegetation_areas.shp')
    gdf.to_file(vegetation_shapefile)

    print(f"Extracted vegetation areas saved to: {vegetation_shapefile}")

# Function to select files using file dialog
def select_file(title):
    file_path = filedialog.askopenfilename(title=title, filetypes=[("GeoTIFF files", "*.TIF")])
    return file_path

# Function to create the output folder with a meaningful name
def create_output_folder():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join('C:/Users/User/Desktop/sat_feat/outputs', f'NDVI_output_{timestamp}')
    os.makedirs(output_dir)  # Create the folder
    return output_dir

# Main GUI window setup
def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Step 1: Select Red (Band 4) and NIR (Band 5) files
    red_band_path = select_file("Select the Red Band (Band 4) Image")
    nir_band_path = select_file("Select the NIR Band (Band 5) Image")

    # Step 2: Calculate NDVI
    ndvi_result, src = calculate_ndvi(red_band_path, nir_band_path)

    # Step 3: Create output folder and save NDVI image
    output_folder = create_output_folder()
    output_file_path = os.path.join(output_folder, 'NDVI_output.tif')
    with rasterio.open(output_file_path, 'w', driver='GTiff', count=1, dtype='float32',
                       width=ndvi_result.shape[1], height=ndvi_result.shape[0],
                       crs=src.crs, transform=src.transform) as dst:
        dst.write(ndvi_result, 1)  # Write the NDVI data to the GeoTIFF
    print(f"NDVI GeoTIFF saved to: {output_file_path}")

    # Step 4: Classify NDVI image
    classified_file_path = filedialog.asksaveasfilename(defaultextension=".tif", filetypes=[("GeoTIFF files", "*.TIF")])
    classified_image = classify_ndvi(ndvi_result, classified_file_path, src.crs, src.transform)

    # Step 5: Extract features from classified image
    extract_features(classified_image, output_folder, src.crs, src.transform)

if __name__ == "__main__":
    main()
