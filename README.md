# pathology-image-tiling-and-correction

## Running this app locally
Run the app locally with: `uvicorn tileImageAndCorrect:app --reload --host "0.0.0.0"`

## Building the container image

1. Clone this repository
1. Inside the directory for this repository, run:

    docker build -t pathology-image-tiling-and-correction

## Running the container
Run the app in Docker via:

    docker run -d -p 8000:8000 pathology-image-tiling-and-correction:latest
