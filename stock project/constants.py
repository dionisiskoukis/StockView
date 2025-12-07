# =====================================================================================================
# CONSTANTS.PY - Configuration and Theme Settings
# =====================================================================================================
# This file contains all the configuration values, color themes, and stock lists used throughout
# the application. By keeping these in one place, it's easy to customize the app's appearance
# and behavior without touching the main code.
# =====================================================================================================

# =====================================================================================================
# COLOR THEME - Modern Dark Professional Look
# =====================================================================================================
# These colors create a professional dark theme with good contrast for readability
# The theme uses dark backgrounds with bright text and accent colors for status indicators

# Main background color - dark blue-gray used for the overall window
BACKGROUND_COLOR = "#0f172a"

# Frame background - slightly lighter for main content areas
FRAME_BG = "#1e293b"

# Card background - used for individual stock cards
CARD_BG = "#334155"

# Text color - bright white for excellent contrast on dark backgrounds
TEXT_COLOR = "#ffffff"

# Secondary text - slightly dimmed for less important information
SECONDARY_TEXT = "#cbd5e1"

# Green color - indicates price went UP (profit/positive change)
GREEN_UP = "#10b981"

# Red color - indicates price went DOWN (loss/negative change)
RED_DOWN = "#ef4444"

# Gray color - indicates price stayed the SAME (no change)
GRAY_NEUTRAL = "#64748b"

# Blue accent color - used for buttons and highlighted elements
BLUE_ACCENT = "#3b82f6"

# Border color - subtle lines for visual separation
BORDER_COLOR = "#475569"

# =====================================================================================================
# STOCK LIST - Stocks to Display in the Application
# =====================================================================================================
# This is the list of stock symbols that will be displayed on the main screen
# You can add or remove stock symbols here, and they'll automatically appear in the app
# Each symbol should be the official Yahoo Finance ticker symbol

STOCKS = [
    "AAPL",   # Apple Inc.
    "MSFT",   # Microsoft Corporation
    "NVDA",   # NVIDIA Corporation
    "TSLA",   # Tesla Inc.
    "AMZN",   # Amazon.com Inc.
    "GOOG",   # Alphabet Inc. (Google)
    "META",   # Meta Platforms (Facebook)
    "NFLX",   # Netflix Inc.
    "AMD",    # Advanced Micro Devices
    "INTC",   # Intel Corporation
    "CSCO",   # Cisco Systems
    "ADBE",   # Adobe Inc.
    "CRM",    # Salesforce Inc.
    "ORCL",   # Oracle Corporation
    "IBM",    # International Business Machines
]

# =====================================================================================================
# UPDATE INTERVALS (in milliseconds)
# =====================================================================================================
# These values control how often the app refreshes data from Yahoo Finance
# Lower values = more frequent updates, but more API calls and slower app
# Higher values = less frequent updates, but faster app and fewer API calls

# How often to update stock prices on the main screen (in milliseconds)
# 30 seconds = 30000 milliseconds (good balance between fresh data and performance)
PRICE_UPDATE_INTERVAL = 30000

# How often to update the intraday chart when viewing a stock detail (in milliseconds)
# 60 seconds = 60000 milliseconds (charts don't need to update as frequently)
CHART_UPDATE_INTERVAL = 60000

# =====================================================================================================
# UI LAYOUT SETTINGS
# =====================================================================================================
# These settings control the appearance and layout of the user interface

# Number of columns in the stock card grid on the main screen
# 3 columns = 3 stocks per row (looks good on most screens)
GRID_COLUMNS = 3

# Font family used throughout the app
# "Segoe UI" is a modern, clean font that looks good on Windows
FONT_NAME = "Segoe UI"

# Font size for stock price labels (in points)
STOCK_PRICE_FONT_SIZE = 16

# Font size for stock symbol labels (in points)
STOCK_SYMBOL_FONT_SIZE = 14

# Font size for detail view information (in points)
DETAIL_FONT_SIZE = 12

# =====================================================================================================
# WINDOW DIMENSIONS
# =====================================================================================================
# These values set the initial size of the application window

# Initial window width (in pixels)
WINDOW_WIDTH = 1400

# Initial window height (in pixels)
WINDOW_HEIGHT = 900
