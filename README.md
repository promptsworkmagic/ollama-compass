# Thanks Ollama

**Thanks Ollama** is a Python toolset that discovers, analyzes, and serves information about publicly exposed Ollama LLM instances. It uses Shodan to find hosts, stores the data in a local SQLite database, and provides an interactive web interface to manage and view the data.

This tool is designed for researchers and security analysts who want to map and monitor the exposure of open LLM endpoints on the internet.

---

## Acknowledgements

This project is a fork of the original [ollama-hunter](https://github.com/saadi1995/ollama-hunter) project by [saadi1995](https://github.com/saadi1995). While this version has been modified and disconnected from the original fork network, we gratefully acknowledge the foundational work of the original author.

---

## Features

-   **Web-Based Management**: A fully interactive web UI to run discovery scans, refresh host data, and view results.
-   **Interactive Data Table**: View all live hosts in a clean, sortable, and filterable table.
-   **Dynamic Sorting**: Sort hosts by "Last Seen" or "Probable Performance" in both ascending and descending order.
-   **Model Filtering**: Dynamically filter the host list to show only hosts running specific, user-selected models.
-   **Background Task Execution**: Discovery and refresh scans are run as background processes, allowing the UI to remain responsive.
-   **Database Storage**: Saves all discovered hosts, their country, and their models to a persistent SQLite database (`ollama_hosts.db`).
-   **JSON API**: In addition to the UI, data is available at `/api/providers` for integration with other tools.

---

## Setup and Usage

### 1. Environment Setup

It is recommended to run this project in a Python virtual environment.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### 2. Installation

Install the required Python libraries using `pip`.

```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Application

**A. Initialize the Database (First-Time Setup)**

Before the first run, initialize the SQLite database:

```bash
python database.py
```

**B. Start the Web Service**

This single command starts the web application.

```bash
python provider-service.py
```

Navigate to **`http://127.0.0.1:5000`** in your web browser to access the main interface.

### 4. Using the Web Interface

-   **Run Thanks Ollama**: To discover new hosts, enter your Shodan `polito` cookie value in the input field and click "Run Thanks Ollama". The scan will start in the background. Refresh the page after a few moments to see new results.
-   **Refresh Live Hosts**: Click the "Refresh Live Hosts" button to start a background task that checks the status of all hosts in the database.
-   **Filter and Sort**: Use the filter dropdown to select one or more models and click "Filter". Click on the "Last Seen" or "Probable Performance" table headers to sort the results.

### Command-Line Utilities

While the primary interface is now web-based, the following command-line utilities are still available:

-   **`interrogate-host.py <IP_ADDRESS>`**: Query a single host and save its details to the database.
-   **`test-ollama-host.py <IP_ADDRESS> <MODEL_NAME>`**: Test a specific model on a remote host.