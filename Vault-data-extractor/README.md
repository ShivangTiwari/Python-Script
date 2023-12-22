
## Introduction

This project is designed to extract data from a Vault server using Python scripts. It utilizes the `hvac` library and `requests` module to interact with the Vault server and retrieve secrets or metadata.

## Features

- Fetches keys and values from specified Vault resources.
- Writes retrieved data to a CSV file for analysis or processing.

## Prerequisites

- Python 3.x installed
- Required Python libraries: `hvac`, `requests`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/your_repository.git
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Update the `main.py` file with appropriate Vault URL, token, and other necessary configurations.
2. Run the `main.py` script:

    ```bash
    python main.py
    ```

## Configuration

- **Vault URL**: Replace `vault_url` variable in `main.py` with the URL of your Vault server.
- **Vault Token**: Replace `vault_token` variable in `main.py` with your Vault access token.
- **Adjustment of Vault Paths**: Modify the script logic in `main.py` if your Vault path structure differs.

## Examples

- Extracting data from Vault and generating CSV output.


