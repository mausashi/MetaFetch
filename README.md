# FetchSave

## Overview

**FetchSave** is a command-line Python program designed to fetch web pages, save them to disk, and provide metadata about the fetched content, such as the number of links and images on the page. The program also supports creating a local mirror by downloading the assets (e.g., images, scripts, stylesheets) and updating the links in the HTML file so that the page can be browsed offline.

### Features

- Fetch multiple web pages and save them as `.html` files.
- Collect metadata: number of links, images, and the last fetch timestamp.
- Download and store assets (e.g., images, CSS, JavaScript) locally for offline viewing.
- Optional metadata output via the `--metadata` flag.
- Dockerized environment for easy portability and setup.

## Requirements

The project uses the following Python libraries:
- `requests`
- `beautifulsoup4`

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

Alternatively, you can run the project using Docker (see below).

# Usage
Running the Program
To fetch and save a webpage, run:

```bash
python fetchSave.py <url1> <url2> ...
```
Example:

```bash
python fetchSave.py https://www.google.com https://www.example.com
```
## Fetch with Metadata

To fetch a webpage and display metadata (number of links, images, and last fetch time), use the --metadata option:

```bash
python fetchSave.py --metadata <url1> <url2> ...
```
Example:

```bash
python fetchSave.py --metadata https://www.google.com
```

## Docker Setup
You can also run this project in a Docker container to avoid platform differences.

Build the Docker image:
```bash
docker build -t fetchsave-app .
```
Run the Docker container with local volume mapping:
To save the output on your local machine, run the container with the -v flag to map the host directory (where you want to store the output) to the container's output directory (/app/output):

```bash
docker run -it --rm -v <host_output_directory>:/app/output fetchsave-app --metadata <url1> <url2>
```
Replace <host_output_directory> with the path to the directory on your machine where you want the fetched web pages and assets to be saved.
Example:
```bash
docker run -it --rm -v /path/to/local/directory:/app/output fetchsave-app --metadata https://www.google.com https://autify.com
```
This command fetches the web pages, downloads assets, and saves the results in your specified output directory on your local machine.

## Running Tests

To run the unit tests, use the following command:

```bash
python -m unittest test_fetchSave.py
```
The tests cover key functions such as fetch_url(), collect_metadata(), sanitize_filename(), and error handling scenarios.

Project Structure
```bash
/FetchSave
    |- fetchSave.py           # Main script to fetch web pages and assets
    |- test_fetchSave.py      # Unit tests for the project
    |- requirements.txt       # Python dependencies
    |- Dockerfile             # Docker setup file
```
