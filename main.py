import sys
from PySide6.QtCore import Qt, Slot, QUrl
from PySide6.QtGui import QAction, QIcon, QPixmap, QFont, QDesktopServices
from PySide6.QtWidgets import (
    QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMessageBox,
    QDialog, QPushButton, QMainWindow, QSizePolicy, QGridLayout, QInputDialog
)
import requests
import random
import matplotlib.pyplot as plt
import numpy as np

# Google OAuth configuration
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8000"  # Change to your redirect URI
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
SCOPE = "profile email"

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setStyleSheet("background-color: #FFFFFF;")  # White background
        
        # Background image
        bg_image = QLabel(self)
        bg_image.setPixmap(QPixmap("login_background.jpg"))  # Path to your background image
        bg_image.setGeometry(0, 0, 400, 300)  # Set geometry to cover the entire window
        
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("color: #000000; font-size: 16px; font-weight: bold;")  # Black text
        self.username_edit = QLineEdit()
        self.username_edit.setStyleSheet("color: #000000; font-size: 16px;")  # Black text
        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("color: #000000; font-size: 16px; font-weight: bold;")  # Black text
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet("color: #000000; font-size: 16px;")  # Black text
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: #007AFF; color: #000000; font-size: 16px; " "font-weight: bold;")  # Blue button with black text
        self.login_button.clicked.connect(self.login)

        self.google_button = QPushButton("Login with Google")
        self.google_button.setStyleSheet("background-color: #dd4b39; color: #ffffff; font-size: 16px; " "font-weight: bold;")  # Red button with white text
        self.google_button.clicked.connect(self.login_with_google)
        
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(self.google_button)
        self.setLayout(layout)
    
    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        # Perform validation, for simplicity, we'll just check if both fields are not empty
        if username and password:
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please enter both username and password.")

    def login_with_google(self):
        oauth_url = f"{AUTHORIZATION_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}"
        QDesktopServices.openUrl(QUrl(oauth_url))

class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0  # Dummy Data
        self._data = {"Water": 24, "Rent": 1000, "Coffee": 30, "Grocery": 300, "Phone": 45, "Internet": 70}
        
        # Left Widget
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Right Widget
        self.clear = QPushButton("Clear")
        self.clear.setStyleSheet("font-size: 16px; font-weight: bold; background-color: #007AFF; color: #000000;")
        self.quit = QPushButton("Quit")
        self.quit.setStyleSheet("font-size: 16px; font-weight: bold; background-color: #007AFF; color: #000000;")
        self.plot = QPushButton("Plot Pie Chart")
        self.plot.setStyleSheet("font-size: 16px; font-weight: bold; background-color: #007AFF; color: #000000;")
        self.plot_histogram = QPushButton("Plot Histogram")
        self.plot_histogram.setStyleSheet("font-size: 16px; font-weight: bold; background-color: #007AFF; " "color: #000000;")
        self.recommend = QPushButton("Recommendations")
        self.recommend.setStyleSheet("font-size: 16px; font-weight: bold; background-color: #007AFF; " "color: #000000;")
        self.website_link = QLabel('<a href="https://expense-tracker-78e2whe.gamma.site/">Check out more on the Expense tracker website</a>')
        self.website_link.setStyleSheet("color: #007AFF; font-size: 16px;")  # Blue link color
        self.website_link.setOpenExternalLinks(True)
        
        self.right = QVBoxLayout()
        self.right.addWidget(self.plot)
        self.right.addWidget(self.plot_histogram)
        self.right.addWidget(self.table)
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)
        self.right.addWidget(self.recommend)
        self.right.addWidget(self.website_link)
        
        # Set the layout to the QWidget
        self.setLayout(self.right)
        
        # Signals and Slots
        self.quit.clicked.connect(self.quit_application)
        self.plot.clicked.connect(self.plot_pie_chart)
        self.plot_histogram.clicked.connect(self.plot_histogram_chart)
        self.clear.clicked.connect(self.clear_table)
        self.recommend.clicked.connect(self.get_recommendations)
        
        # Fill example data
        self.fill_table()
    
    @Slot()
    def add_element(self):
        description, ok1 = QInputDialog.getText(self, 'Add Description', 'Enter Description:')
        price, ok2 = QInputDialog.getDouble(self, 'Add Price', 'Enter Price:')
        if ok1 and ok2:
            try:
                price_item = QTableWidgetItem(f"{price:.2f}")
                price_item.setTextAlignment(Qt.AlignRight)
                self.table.insertRow(self.items)
                description_item = QTableWidgetItem(description)
                self.table.setItem(self.items, 0, description_item)
                self.table.setItem(self.items, 1, price_item)
                self.items += 1
            except ValueError:
                print("That is not an invalid input:", price, "Make sure to enter a price!")
    
    @Slot()
    def plot_pie_chart(self):
        # Get table information
        labels = [self.table.item(i, 0).text() for i in range(self.table.rowCount())]
        sizes = [float(self.table.item(i, 1).text()) for i in range(self.table.rowCount())]
        # Plotting the pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Expense Distribution', fontsize=16, fontweight='bold')
        plt.show()
    
    @Slot()
    def plot_histogram_chart(self):
        # Get table information
        labels = [self.table.item(i, 0).text() for i in range(self.table.rowCount())]
        values = [float(self.table.item(i, 1).text()) for i in range(self.table.rowCount())]
        # Plotting the histogram
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.xlabel('Expenses', fontsize=14, fontweight='bold')
        plt.ylabel('Amount', fontsize=14, fontweight='bold')
        plt.title('Expense Histogram', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
    
    @Slot()
    def quit_application(self):
        QApplication.quit()
    
    def fill_table(self, data=None):
        data = self._data if not data else data
        for desc, price in data.items():
            description_item = QTableWidgetItem(desc)
            price_item = QTableWidgetItem(f"{price:.2f}")
            price_item.setTextAlignment(Qt.AlignRight)
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, description_item)
            self.table.setItem(self.items, 1, price_item)
            self.items += 1
    
    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0
    
    @Slot()
    def get_recommendations(self):
        # Placeholder for recommendation logic
        recommendations = ["Reduce dining out expenses", "Cancel unused subscriptions", "Shop for groceries at discounted stores"]
        QMessageBox.information(self, "Recommendations", "\n".join(recommendations), QMessageBox.Ok, QMessageBox.Ok)


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Expense Tracker")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #0000;")  # Light gray background
        # Set widget
        self.setCentralWidget(widget)


# Your existing code goes here...

if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon("F:/CERTIFICATES/image.png"))  # Path to your application icon
    login = LoginWindow()
    if login.exec() == QDialog.Accepted:
        # QWidget
        widget = Widget()
        # QMainWindow using QWidget as central widget
        window = MainWindow(widget)
        window.show()
    # Execute application
    sys.exit(app.exec())
