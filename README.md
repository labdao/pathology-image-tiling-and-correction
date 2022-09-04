# pathology-image-tiling-and-correction

## Running this app locally
Run the app locally with: `uvicorn tileImageAndCorrect:app --reload --host "0.0.0.0"`

## Building the container image

1. Clone this repository
1. Inside the directory for this repository, run:

    ```shell
    docker build -t pathology-image-tiling-and-correction .
    ```

## Running the container
Run the app in Docker via:

    docker run -d -p 8000:8000 pathology-image-tiling-and-correction:latest

and it should be running at http://localhost:8000 (or replace `localhost` with the IP/DNS name of whichever computer is running the container)

## Processing data with Postman

1. In Postman, craft a request with the following properties:

    | Postman parameter | Value |
    | --- | --- |
    | Request Type | `POST` |
    | Body Type | `form-data` |
    | key type (dropdown) | File |
    | key name (textbox) | `files` |
    | key value | (select an image) |
  
1. Press the "Send" button
1. The result should be a .zip file, so when the result is ready (it will look like random letters and numbers in the bottom half of the screen), press "Save Response" on the right side of the screen. Save the zip file.
