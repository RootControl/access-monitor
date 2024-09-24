# Access Monitor

This Python script uses the AccessMonitor tool to retrieve accessibility scores for a set of websites. It provides functionality to take screenshots of the accessibility reports and save the results in an Excel file.

## Features

- Retrieves accessibility scores for multiple websites from the AccessMonitor tool
- Optionally takes screenshots of the accessibility reports
- Saves the results (URL and score) in an Excel file

## Prerequisites

- Python 3.x
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/access-monitor.git
   cd access-monitor
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Download the appropriate ChromeDriver for your system and update the `chrome_driver_path` variable in the `accessibility.py` script.

## Usage

1. Prepare an Excel file (e.g., `input.xlsx`) with a column named "URL" containing the websites you want to analyze.

2. Run the script with the input file path:
   ```
   python accessibility.py input.xlsx
   ```

   Optional flags:
   - `-s`: Take screenshots of the accessibility reports

3. The script will:
   - Process the URLs from your input file
   - Retrieve the accessibility score for each URL
   - Optionally take a screenshot of each accessibility report
   - Save the results (URL and score) in a new Excel file named `New_input.xlsx`

## Configuration

You can modify the following constants in the `accessibility.py` script:

- `chrome_driver_path`: The path to the ChromeDriver executable
- `seconds_between_requests`: The number of seconds to wait between requests to the AccessMonitor tool
- `seconds_to_get_result`: The number of seconds to wait for the accessibility score to be generated
- `seconds_to_screenshot`: The number of seconds to wait for the screenshot to be taken

## Output

The script generates two types of output:

1. An Excel file (`New_input.xlsx`) containing:
   - URL
   - Accessibility score

2. Screenshots of the accessibility reports, saved in the `screenshots/` directory (if the `-s` flag is used).

## Troubleshooting

- If you encounter issues with ChromeDriver, ensure that its version is compatible with your installed Chrome browser.
- Make sure you have the necessary permissions to read the input file and write to the output directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
