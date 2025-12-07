# 📈 Modern Stock Viewer 📊

A sleek and modern stock price viewer application built with Python, Tkinter, and Matplotlib. This project provides a user-friendly interface to track stock prices, view historical charts, and get detailed stock information. It fetches real-time data from Yahoo Finance, offering a near real-time view of the market.

## 🚀 Key Features

- **Real-time Stock Prices:** Fetches and displays current stock prices, indicating whether the price has increased or decreased.
- **Interactive Stock Cards:** Presents stock information in visually appealing cards, making it easy to scan and select stocks.
- **Dynamic Charts:** Generates and displays interactive stock price charts using historical data.
- **Detailed Stock Information:** Provides detailed information for selected stocks, offering a deeper dive into company performance.
- **Modern UI:** Utilizes `tkinter.ttk` for a modern and visually appealing user interface.
- **Customizable:** Uses a `constants.py` file for easy customization of colors, settings, and stock list.
- **Data Abstraction:** Separates data fetching logic into `stock_data.py` for better maintainability and testability.

## 🛠️ Tech Stack

- **Frontend:**
    - `tkinter`:  For creating the main application window and basic UI elements.
    - `tkinter.ttk`: For themed widgets, providing a more modern look and feel.
- **Charting:**
    - `matplotlib.figure.Figure`: For creating matplotlib figures to display stock charts.
    - `matplotlib.backends.backend_tkagg.FigureCanvasTkAgg`: To embed matplotlib figures into a Tkinter window.
    - `matplotlib.dates.DateFormatter`: To format dates on the x-axis of the stock charts.
    - `matplotlib.pyplot`: For creating plots.
- **Backend:**
    - `yfinance`: A Python library used to access the Yahoo Finance API.
    - `datetime`: A Python module used for working with dates and times.
- **Data Management:**
    - `stock_data.StockDataManager`: Custom class for fetching and managing stock data.
- **Configuration:**
    - `constants.py`:  For defining colors, settings, and the list of stocks to display.

## 📦 Getting Started

### Prerequisites

- Python 3.x
- Required Python packages: `tkinter`, `tkinter.ttk`, `matplotlib`, `yfinance`

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Install the required packages using pip:

    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Create a `requirements.txt` file with the following content if it doesn't exist)*
    ```
    yfinance
    matplotlib
    ```

### Running Locally

1.  Navigate to the project directory.
2.  Run the `main.py` file:

    ```bash
    python main.py
    ```

## 💻 Usage

The application will launch, displaying a grid of stock cards with real-time price updates and charts. Click on a stock card to view detailed information about the selected stock.

## 📂 Project Structure

```
stock project/
├── main.py           # Main application file with UI and logic
├── stock_data.py     # File for fetching stock data from Yahoo Finance
├── constants.py      # File for defining constants like colors and stock list
└── requirements.txt  # Lists project dependencies
```

## 📸 Screenshots

*(Add screenshots of the application here to showcase its UI and features)*

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Submit a pull request.

## 📝 License

This project is licensed under the [MIT License](LICENSE) - see the `LICENSE` file for details.

## 📬 Contact

If you have any questions or suggestions, feel free to contact me at [your_email@example.com](mailto:koukisdionisis@gmail.com).

