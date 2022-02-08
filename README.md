# pingpi

[![CI](https://github.com/lsetiawan/pingpi/actions/workflows/ci.yaml/badge.svg)](https://github.com/lsetiawan/pingpi/actions/workflows/ci.yaml)

Ping API for uploading and reading back the pings.csv given

## Development

1. Install the whole package

    ```bash
    pip install -e .[all]
    ```

2. Run with uvicorn

    ```bash
    uvicorn pingpi.main:app --reload
    ```

## Current deployment

Heroku: https://peaceful-bayou-22452.herokuapp.com/
