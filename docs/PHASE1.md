# Phase 1. Setup and pre-processing

In this almost-initial phase two main points had been covered: Environment setup and data engineering tasks, including:

- Data extract from Google Earth Engine, SPAM and AOIs
- Data transformation (raster data vectorization)
- Data load into the database

## Environment setup

A Docker-Compose based environment has been chosen for this project. Please find detailed information on this setup, how to build and run it [here](../env/).

## Data engineering tasks

#### Vector vs Raster choice

Vector format has been preferred over raster for the following reasons:

1. Data structure. Structured data opens a world of possibilities (think of relating one image to another based a field as it can be done with tables in a relational database)

2. Geospatial operations. Even though vector data has a higher computational cost, it allows leveraging several potentially interesting geospatial functions (e.g: clustering algorithms, KNN, intersections, etc).

3. Possibility of integration with other vector data sources. At this stage, I did not have a clear idea of which data sources could serve best to contextualize the SPAM dataset and hence preferred a vector format.

4. Visualization. Even though in the end no complex visualizations had been crafted, vector data is generally preferred in this sense (e.g: for 3D visualizations, etc)

### Data extract

Data download for AOIs (areas dataset) and SPAM has been straightforward. The SPAM dataset had been downloaded in CSV format containing pixel centroids in lat/long format.

Two additional data sources have been downloaded from Google Earth Engine (GEE) using simple JS scripts from the GEE console: Burned area and Forest loss information, both intended to be used as boolean parameters for aggregated grid cells (more context in Phase 2).

Please find more information on this topic [here](../env/notebooks/scripts/extract/).

### Data transform (pre-load)

Before loading the raster datasets from GEE into the database, these have been vectorized using Python bindings for GDAL, through the script defined [here](../env/notebooks/scripts/transform/).

>:memo: **NOTE:** Vectorizing raster data sources can lead to artifacts and even invalid geometries. While it'd be possible to introduce a random seed to keep each pixel as a single geometry, in this case the idea was to finally aggregate data in a grid, and therefore the choice has been to simply validate geometries afterwards.

### Data load

In order to load data into the database, a Bash script that uses [`ogr2ogr` tool](https://gdal.org/programs/ogr2ogr.html) has been created. Please find the script [here](../env/notebooks/scripts/load/).


### Data transform (post-load)

After loading the data into the database, an additional step to inspect it and post-process it to ensure data quality has been performed.

This step has been performed through a Jupyter Notebook that already leverages the `research` Python package crafted for this project.

Please see the corresponding Jupyter Notebook [here](../env/notebooks/Step%201.%20Pre-processing.ipynb). A walkthrough GIF of this process is also included below.

![Pre-processing](../env/notebooks/img/step_1_preprocessing_walkthrough.gif)

## What's next?

Please see the [Phase 2. Analysis & Conclusions](PHASE2.md)