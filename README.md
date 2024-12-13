Satellite Imagery NDVI Classification and Feature Extraction
============================================================

This Python script automates the process of **NDVI calculation**, **land-use classification**, and **feature extraction** from satellite imagery. It uses the **Red** and **Near-Infrared (NIR)** bands of satellite images to calculate NDVI, classifies the image into categories (vegetation, water, barren land), and extracts polygons of each category as a **shapefile**.

Key Features:
-------------

1.  **NDVI Calculation**: Computes the Normalized Difference Vegetation Index (NDVI) using satellite imagery.
2.  **Image Classification**: Classifies NDVI values into **vegetation**, **water**, and **barren land** categories.
3.  **Feature Extraction**: Converts the classified raster data into **vector polygons** for vegetation areas, water bodies, and barren land, and saves them as a **shapefile**.
4.  **User-Friendly GUI**: Provides an easy-to-use graphical user interface (GUI) for users to select files and save results without needing programming knowledge.

Libraries Used:
---------------

-   **rasterio**: For reading and processing raster data (satellite imagery).
-   **numpy**: For numerical calculations and data manipulation.
-   **matplotlib**: For visualizing NDVI and classification results.
-   **geopandas**: For creating and saving shapefiles from the classified data.
-   **tkinter**: For creating the GUI that allows users to select files and directories.

How It Works:
-------------

1.  **Step 1**: User selects the **Red (Band 4)** and **Near-Infrared (Band 5)** satellite bands.
2.  **Step 2**: The script calculates **NDVI** from these bands.
3.  **Step 3**: The NDVI image is classified into three categories:
    -   **Vegetation** (NDVI > 0.3)
    -   **Water** (NDVI < 0.1)
    -   **Barren Land** (0.0 <= NDVI < 0.3)
4.  **Step 4**: The classified image is saved as a **GeoTIFF**.
5.  **Step 5**: Polygons representing the classified categories (e.g., vegetation areas) are extracted and saved as a **shapefile** for further analysis in GIS tools (e.g., QGIS or ArcGIS).

How to Run the Script:
----------------------

### Requirements:

-   Python 3.x
-   The following Python libraries:
    -   rasterio
    -   numpy
    -   matplotlib
    -   geopandas
    -   tkinter (comes with Python)

You can install the required libraries using **pip**:

bash

Copy code

`pip install rasterio numpy matplotlib geopandas`

### Running the Script:

1.  Clone this repository to your local machine.
2.  Run the script using Python:

    bash

    Copy code

    `python satellite_processing.py`

    This will launch the **GUI** that will guide you through:
    -   Selecting the **Red** and **NIR** bands for NDVI calculation.
    -   Saving the **NDVI** GeoTIFF.
    -   Classifying the NDVI image into vegetation, water, and barren land.
    -   Extracting polygons and saving them as a shapefile.

### Expected Outputs:

1.  **NDVI GeoTIFF**: A GeoTIFF file containing the NDVI values.
2.  **Classified GeoTIFF**: A GeoTIFF file showing the classification results (vegetation, water, barren land).
3.  **Shapefile**: A shapefile containing the polygons for vegetation areas (or other categories) extracted from the classified image.

### Example Outputs:

-   **NDVI GeoTIFF**: Contains normalized values from -1 to 1, where positive values represent vegetation.
-   **Classified GeoTIFF**: A categorized image where different land use classes (vegetation, water, barren land) are represented with unique integer values.
-   **Shapefile**: Contains vector polygons of the classified land use categories, which can be opened in QGIS or any GIS tool.

Use Cases:
----------

-   **Environmental Monitoring**: Detect deforestation, track vegetation health, or monitor water bodies.
-   **Agriculture**: Monitor crop health and growth.
-   **Urban Planning**: Analyze land-use patterns, including urban and vegetation areas.
-   **Water Resources**: Study the dynamics of water bodies over time.
-   **Disaster Response**: Assess the impact of natural disasters such as floods or wildfires on vegetation and land.

License:
--------

This project is licensed under the **MIT License** - see the LICENSE file for details.