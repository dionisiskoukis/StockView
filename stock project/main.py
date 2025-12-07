# =====================================================================================================
# MAIN.PY - Main Application UI and Logic
# =====================================================================================================
# This is the main application file that creates the user interface and orchestrates everything.
# It imports from constants.py (for colors and settings) and stock_data.py (for data fetching).
# This file handles:
#   - Creating the main window
#   - Displaying stock cards in a grid
#   - Handling user interactions (clicking stocks)
#   - Updating prices and charts
#   - Showing detailed stock information
# =====================================================================================================

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt

# Import from our other files
from constants import *  # Import all colors, settings, and stock list
from stock_data import StockDataManager  # Import the data fetcher class

# =====================================================================================================
# MAIN APPLICATION CLASS
# =====================================================================================================
# This is the main class that creates and manages the entire application
# All UI elements and logic are organized within this class

class ModernStockViewer:
    """
    Main application class that creates the stock viewer interface.
    This class handles:
    - Creating the main window
    - Managing frames (main view vs detail view)
    - Creating and updating stock cards
    - Displaying charts and information
    """

    # ===============================================================================================
    # CONSTRUCTOR - Runs when we create a new ModernStockViewer
    # ===============================================================================================
    def __init__(self, root):
        """
        Initialize the main application.

        Parameters:
            root: The tkinter root window
        """
        # Store the root window
        self.root = root

        # Set up the window title and size
        self.root.title("Bloomberg Terminal - Stock Price Viewer")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Create a StockDataManager instance to fetch stock data
        # We'll use this throughout the app to get prices, charts, and info
        self.data_manager = StockDataManager()

        # Dictionary to store label widgets for each stock
        # We use this to update prices without recreating the labels
        # Example: self.stock_labels['AAPL'] = the label widget for AAPL
        self.stock_labels = {}

        # Dictionary to store the detail frame for each stock
        # When the user clicks a stock, we show its detail frame
        self.detail_frames = {}

        # Dictionary to store matplotlib charts for each stock
        # We keep these in memory to update them without recreating
        self.charts = {}

        # Dictionary to store the canvases (chart display areas)
        self.canvases = {}

        # Set up the main view (the grid of stock cards)
        self.setup_main_frame()

        # Create hidden detail frames for each stock
        # These frames are hidden until the user clicks a stock
        self.create_detail_frames()

        # Show the main view first
        self.show_main_view()

        # Schedule the first price update
        # This will run every PRICE_UPDATE_INTERVAL milliseconds (e.g., 30 seconds)
        self.update_prices()

    # ===============================================================================================
    # METHOD: Set Up Main Frame
    # ===============================================================================================
    def setup_main_frame(self):
        """
        Create the main view with scrollable grid of stock cards.

        This method:
        1. Creates a scrollable frame using Canvas and Scrollbar
        2. Creates a grid layout with stock cards
        3. Makes it responsive so the app looks good on different screen sizes
        """

        # Create a frame to hold everything
        self.main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas for scrolling
        # This allows us to have more stocks than fit on the screen
        # The user can scroll down to see all stocks
        self.canvas = tk.Canvas(self.main_frame, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Connect the scrollbar to the canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the stock cards
        # This frame will scroll when the user scrolls the canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # When the scrollable frame changes size, update the canvas scroll region
        # This ensures the scrollbar works correctly
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Allow mouse wheel scrolling
        # This is a nice user experience feature
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Create the stock card grid
        self.create_stock_grid()

    # ===============================================================================================
    # METHOD: Create Stock Card Grid
    # ===============================================================================================
    def create_stock_grid(self):
        """
        Create a grid of stock cards arranged in columns.

        This method:
        1. Creates rows and columns in the scrollable frame
        2. Creates a card for each stock
        3. Arranges them so they look nice (3 columns)
        """

        # Loop through each stock in the stock list
        for idx, stock in enumerate(STOCKS):
            # Calculate which row and column this stock should be in
            # idx = 0, 1, 2 -> row 0 (first three stocks in first row)
            # idx = 3, 4, 5 -> row 1 (next three stocks in second row)
            # etc.
            row = idx // GRID_COLUMNS
            col = idx % GRID_COLUMNS

            # Create a card for this stock
            self.create_stock_card(stock, row, col)

    # ===============================================================================================
    # METHOD: Create a Single Stock Card
    # ===============================================================================================
    def create_stock_card(self, symbol, row, col):
        """
        Create a single stock card with price display.

        Parameters:
            symbol (str): The stock symbol (e.g., "AAPL")
            row (int): The row position in the grid
            col (int): The column position in the grid

        This method creates a card that shows:
        - Stock symbol (e.g., "AAPL")
        - Current price (e.g., "$150.25")
        - Color indicator (green = up, red = down, gray = same)
        - Clickable so user can see details
        """

        # Create a frame for the card
        # This frame will hold the symbol and price labels
        card_frame = tk.Frame(self.scrollable_frame, bg=CARD_BG, relief=tk.FLAT)
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # Make the card expand to fill available space
        self.scrollable_frame.grid_columnconfigure(col, weight=1)

        # Create the stock symbol label (e.g., "AAPL")
        symbol_label = tk.Label(
            card_frame,
            text=symbol,
            font=(FONT_NAME, STOCK_SYMBOL_FONT_SIZE, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        symbol_label.pack(pady=(15, 5))

        # Create the price label (this will be updated later)
        # We'll update this label every 30 seconds with the new price
        price_label = tk.Label(
            card_frame,
            text="Loading...",
            font=(FONT_NAME, STOCK_PRICE_FONT_SIZE, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        price_label.pack(pady=(5, 15))

        # Store the price label in our dictionary so we can update it later
        self.stock_labels[symbol] = price_label

        # Make the card clickable
        # When the user clicks on any part of the card, show the detail view for that stock
        for widget in [card_frame, symbol_label, price_label]:
            widget.bind("<Button-1>", lambda e, s=symbol: self.show_detail_view(s))
            # Change cursor to hand when hovering over card (shows it's clickable)
            widget.bind("<Enter>", lambda e: self._set_cursor_hand(e))
            widget.bind("<Leave>", lambda e: self._set_cursor_arrow(e))

    # ===============================================================================================
    # METHOD: Change Cursor to Hand (for hovering)
    # ===============================================================================================
    def _set_cursor_hand(self, event):
        """Change cursor to hand pointer on hover."""
        event.widget.config(cursor="hand2")

    # ===============================================================================================
    # METHOD: Change Cursor Back to Arrow
    # ===============================================================================================
    def _set_cursor_arrow(self, event):
        """Change cursor back to arrow."""
        event.widget.config(cursor="arrow")

    # ===============================================================================================
    # METHOD: Create Detail Frames for Each Stock
    # ===============================================================================================
    def create_detail_frames(self):
        """
        Create hidden detail frames for each stock.

        When the user clicks a stock card, we show the detail frame for that stock.
        The detail frame shows:
        - A larger chart of the stock price
        - Detailed information (market cap, P/E ratio, etc.)
        - A back button to return to the main view
        """

        # Loop through each stock
        for symbol in STOCKS:
            # Create a frame for this stock's details
            detail_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
            detail_frame.place(relwidth=1, relheight=1)  # Make it fill the entire window

            # Create a top bar for the stock symbol and back button
            top_bar = tk.Frame(detail_frame, bg=FRAME_BG, height=60)
            top_bar.pack(fill=tk.X)

            # Back button
            back_button = tk.Button(
                top_bar,
                text="← Back to Main",
                font=(FONT_NAME, 12, "bold"),
                bg=BLUE_ACCENT,
                fg=TEXT_COLOR,
                relief=tk.FLAT,
                padx=15,
                pady=10,
                command=self.show_main_view
            )
            back_button.pack(side=tk.LEFT, padx=15, pady=10)

            # Stock symbol label
            symbol_label = tk.Label(
                top_bar,
                text=symbol,
                font=(FONT_NAME, 20, "bold"),
                bg=FRAME_BG,
                fg=TEXT_COLOR
            )
            symbol_label.pack(side=tk.LEFT, padx=15, pady=10)

            # Create a scrollable area for content below the top bar
            content_frame = tk.Frame(detail_frame, bg=BACKGROUND_COLOR)
            content_frame.pack(fill=tk.BOTH, expand=True)

            # Create a canvas for scrolling
            canvas = tk.Canvas(content_frame, bg=BACKGROUND_COLOR, highlightthickness=0)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame inside the canvas to hold the chart and info
            inner_frame = tk.Frame(canvas, bg=BACKGROUND_COLOR)
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            def configure_scroll(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            inner_frame.bind("<Configure>", configure_scroll)

            # Create a frame for the chart
            chart_frame = tk.Frame(inner_frame, bg=BACKGROUND_COLOR)
            chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Create a matplotlib figure for the chart
            # figsize=(12, 4) means the chart will be 12 inches wide and 4 inches tall
            # dpi=100 means 100 dots per inch (higher = more detailed)
            fig = Figure(figsize=(12, 4), dpi=100)
            plot = fig.add_subplot(1, 1, 1)

            # Style the plot to match our dark theme
            fig.patch.set_facecolor(BACKGROUND_COLOR)
            plot.set_facecolor(FRAME_BG)
            plot.tick_params(colors=SECONDARY_TEXT)
            plot.spines['bottom'].set_color(BORDER_COLOR)
            plot.spines['left'].set_color(BORDER_COLOR)
            plot.spines['top'].set_visible(False)
            plot.spines['right'].set_visible(False)

            # Create a canvas to display the matplotlib figure
            canvas_widget = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas_widget.draw()
            canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Store the chart and canvas for later updates
            self.charts[symbol] = (fig, plot)
            self.canvases[symbol] = canvas_widget

            # Create a frame for stock information
            info_frame = tk.Frame(inner_frame, bg=BACKGROUND_COLOR)
            info_frame.pack(fill=tk.BOTH, padx=20, pady=20)

            # Create labels for each piece of information
            # These will be updated when we show the detail view
            info_labels = {}

            # Market Cap label
            market_cap_label = tk.Label(
                info_frame,
                text="Market Cap: Loading...",
                font=(FONT_NAME, DETAIL_FONT_SIZE),
                bg=BACKGROUND_COLOR,
                fg=TEXT_COLOR,
                justify=tk.LEFT
            )
            market_cap_label.pack(anchor="w", pady=5)
            info_labels['market_cap'] = market_cap_label

            # P/E Ratio label
            pe_label = tk.Label(
                info_frame,
                text="P/E Ratio: Loading...",
                font=(FONT_NAME, DETAIL_FONT_SIZE),
                bg=BACKGROUND_COLOR,
                fg=TEXT_COLOR,
                justify=tk.LEFT
            )
            pe_label.pack(anchor="w", pady=5)
            info_labels['pe_ratio'] = pe_label

            # Dividend Yield label
            div_label = tk.Label(
                info_frame,
                text="Dividend Yield: Loading...",
                font=(FONT_NAME, DETAIL_FONT_SIZE),
                bg=BACKGROUND_COLOR,
                fg=TEXT_COLOR,
                justify=tk.LEFT
            )
            div_label.pack(anchor="w", pady=5)
            info_labels['dividend_yield'] = div_label

            # 52-Week High label
            high_52_label = tk.Label(
                info_frame,
                text="52-Week High: Loading...",
                font=(FONT_NAME, DETAIL_FONT_SIZE),
                bg=BACKGROUND_COLOR,
                fg=TEXT_COLOR,
                justify=tk.LEFT
            )
            high_52_label.pack(anchor="w", pady=5)
            info_labels['52_week_high'] = high_52_label

            # 52-Week Low label
            low_52_label = tk.Label(
                info_frame,
                text="52-Week Low: Loading...",
                font=(FONT_NAME, DETAIL_FONT_SIZE),
                bg=BACKGROUND_COLOR,
                fg=TEXT_COLOR,
                justify=tk.LEFT
            )
            low_52_label.pack(anchor="w", pady=5)
            info_labels['52_week_low'] = low_52_label

            # Day High label
            day_high_label = tk.Label(
                info_frame,
                text="Day High: Loading...",
                font=(FONT_NAME, DETAIL_FONT_SIZE),
                bg=BACKGROUND_COLOR,
                fg=TEXT_COLOR,
                justify=tk.LEFT
            )
            day_high_label.pack(anchor="w", pady=5)
            info_labels['day_high'] = day_high_label

            # Day Low label
            day_low_label = tk.Label(
                info_frame,
                text="Day Low: Loading...",
                font=(FONT_NAME, DETAIL_FONT_SIZE),
                bg=BACKGROUND_COLOR,
                fg=TEXT_COLOR,
                justify=tk.LEFT
            )
            day_low_label.pack(anchor="w", pady=5)
            info_labels['day_low'] = day_low_label

            # Store the detail frame and info labels
            self.detail_frames[symbol] = {
                'frame': detail_frame,
                'info_labels': info_labels
            }

    # ===============================================================================================
    # METHOD: Show Main View
    # ===============================================================================================
    def show_main_view(self):
        """
        Show the main view (grid of stock cards).

        This method hides all detail frames and shows the main frame.
        """
        # Hide all detail frames
        for symbol in STOCKS:
            self.detail_frames[symbol]['frame'].place_forget()

        # Show the main frame
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    # ===============================================================================================
    # METHOD: Show Detail View
    # ===============================================================================================
    def show_detail_view(self, symbol):
        """
        Show the detail view for a specific stock.

        Parameters:
            symbol (str): The stock symbol to show details for

        This method:
        1. Shows the detail frame for the stock
        2. Updates the chart with current data
        3. Updates the information labels
        """
        # Hide the main frame
        self.main_frame.pack_forget()

        # Show the detail frame for this stock
        self.detail_frames[symbol]['frame'].place(relwidth=1, relheight=1)

        # Update the chart and information
        self.update_detail_view(symbol)

        # Schedule the chart to update every CHART_UPDATE_INTERVAL milliseconds
        self.root.after(CHART_UPDATE_INTERVAL, lambda: self.update_chart(symbol))

    # ===============================================================================================
    # METHOD: Update Detail View
    # ===============================================================================================
    def update_detail_view(self, symbol):
        """
        Update the chart and information labels for a stock.

        Parameters:
            symbol (str): The stock symbol to update
        """
        # Update the chart
        self.update_chart(symbol)

        # Fetch stock information using the StockDataManager
        info = self.data_manager.get_stock_info(symbol)

        # Update each information label with the fetched data
        info_labels = self.detail_frames[symbol]['info_labels']

        info_labels['market_cap'].config(text=f"Market Cap: {info['market_cap']}")
        info_labels['pe_ratio'].config(text=f"P/E Ratio: {info['pe_ratio']}")
        info_labels['dividend_yield'].config(text=f"Dividend Yield: {info['dividend_yield']}")
        info_labels['52_week_high'].config(text=f"52-Week High: {info['52_week_high']}")
        info_labels['52_week_low'].config(text=f"52-Week Low: {info['52_week_low']}")
        info_labels['day_high'].config(text=f"Day High: {info['day_high']}")
        info_labels['day_low'].config(text=f"Day Low: {info['day_low']}")

    # ===============================================================================================
    # METHOD: Update Chart
    # ===============================================================================================
    def update_chart(self, symbol):
        """
        Update the intraday chart for a stock.

        Parameters:
            symbol (str): The stock symbol to update the chart for

        This method:
        1. Fetches the latest intraday data
        2. Clears the old chart
        3. Plots the new data
        4. Refreshes the canvas to show the new chart
        """
        try:
            # Fetch intraday data using the StockDataManager
            data = self.data_manager.get_intraday_data(symbol)

            # Check if we got valid data
            if data is None or data.empty:
                return

            # Get the chart figure and plot
            fig, plot = self.charts[symbol]

            # Clear the old chart
            plot.clear()

            # Plot the new data
            # data.index contains the timestamps
            # data['Close'] contains the closing prices for each minute
            plot.plot(data.index, data['Close'], color=BLUE_ACCENT, linewidth=2)

            # Fill the area under the line with a semi-transparent blue
            # This creates a nice visual effect
            plot.fill_between(data.index, data['Close'], alpha=0.2, color=BLUE_ACCENT)

            # Set the title
            plot.set_title(f"{symbol} - Intraday Prices", color=TEXT_COLOR, fontsize=14, fontweight='bold')

            # Set the labels
            plot.set_xlabel("Time", color=SECONDARY_TEXT)
            plot.set_ylabel("Price ($)", color=SECONDARY_TEXT)

            # Format the x-axis to show times (not dates)
            # DateFormatter('%H:%M') means show hours and minutes (e.g., "09:30")
            plot.xaxis.set_major_formatter(DateFormatter('%H:%M'))

            # Rotate the x-axis labels so they're readable
            fig.autofmt_xdate(rotation=45)

            # Add a grid for easier reading
            plot.grid(True, alpha=0.2, color=BORDER_COLOR)

            # Style the plot to match our dark theme
            plot.set_facecolor(FRAME_BG)
            plot.tick_params(colors=SECONDARY_TEXT)
            plot.spines['bottom'].set_color(BORDER_COLOR)
            plot.spines['left'].set_color(BORDER_COLOR)
            plot.spines['top'].set_visible(False)
            plot.spines['right'].set_visible(False)

            # Refresh the canvas to show the updated chart
            self.canvases[symbol].draw()

        except Exception as e:
            print(f"Error updating chart for {symbol}: {str(e)}")

    # ===============================================================================================
    # METHOD: Update Prices
    # ===============================================================================================
    def update_prices(self):
        """
        Update the prices for all stocks on the main view.

        This method:
        1. Fetches the current price for each stock
        2. Updates the label with the new price
        3. Colors the label based on whether price went up (green), down (red), or stayed same (gray)
        4. Schedules itself to run again after PRICE_UPDATE_INTERVAL milliseconds
        """
        # Loop through each stock
        for symbol in STOCKS:
            try:
                # Fetch the current price using the StockDataManager
                price_data = self.data_manager.get_current_price(symbol)

                # Check if there was an error
                if price_data['error']:
                    # Show error message in the label
                    self.stock_labels[symbol].config(text=price_data['error'], fg=TEXT_COLOR)
                    continue

                # Get the price
                price = price_data['price']

                # Get the direction (UP, DOWN, or NEUTRAL)
                direction = price_data['direction']

                # Determine the color based on direction
                if direction == 'UP':
                    color = GREEN_UP
                elif direction == 'DOWN':
                    color = RED_DOWN
                else:
                    color = GRAY_NEUTRAL

                # Format the price with 2 decimal places
                price_text = f"${price:.2f}"

                # Update the label
                self.stock_labels[symbol].config(text=price_text, fg=color)

            except Exception as e:
                # If something goes wrong, show an error
                print(f"Error updating price for {symbol}: {str(e)}")

        # Schedule this method to run again after PRICE_UPDATE_INTERVAL milliseconds
        self.root.after(PRICE_UPDATE_INTERVAL, self.update_prices)


# =====================================================================================================
# MAIN EXECUTION
# =====================================================================================================
# This code runs when we execute the script with: python main.py

if __name__ == "__main__":
    # Create the root tkinter window
    root = tk.Tk()

    # Create the application
    app = ModernStockViewer(root)

    # Start the application (this runs forever until the user closes the window)
    root.mainloop()
