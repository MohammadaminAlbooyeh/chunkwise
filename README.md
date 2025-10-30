# Data Analysis Project

This project contains scripts and notebooks for data analysis tasks.

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/data_analysis.git
   cd data_analysis
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```sh
     .venv\Scripts\Activate.ps1
     ```

4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

- Main scripts are located in the `src/` directory.
- Run the main script:
  ```sh
  python src/main.py
  ```

## Project Structure

```
data_analysis/
├── .venv/                # Virtual environment (not tracked by git)
├── src/                  # Source code
│   └── main.py
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

## Notes

- Add `.venv/` to your `.gitignore` file.
- Update `requirements.txt` when you add new dependencies.

## License

MIT License