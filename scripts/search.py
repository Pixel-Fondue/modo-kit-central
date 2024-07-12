import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Search")

        # Create search bar for comma-separated terms
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter comma-separated search terms...")

        # Create search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_database)

        # Create results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.search_button)
        layout.addWidget(self.results_display)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def search_database(self):
        search_input = self.search_bar.text()
        if search_input:
            search_terms = [term.strip() for term in search_input.split(',')]
            results = self.execute_search(search_terms)
            self.display_results(results)

    def execute_search(self, search_terms):
        database = "scripts/resources/test.db"
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        # Base query
        query = "SELECT name, author, version, description, url, help, installable, search FROM kits WHERE 1=1"
        params = []

        # Add conditions for each search term
        for term in search_terms:
            query += " AND (name LIKE ? OR desc LIKE ? OR author LIKE ?)"
            params.extend([f"%{term}%", f"%{term}%", f"%{term}%"])

        cursor.execute(query, params)
        results = cursor.fetchall()
        connection.close()

        return results

    def display_results(self, results):
        self.results_display.clear()
        if results:
            for result in results:
                name, desc, url, help_text, author = result
                self.results_display.append(f"Name: {name}\nDescription: {desc}\nURL: {url}\nHelp: {help_text}\nAuthor: {author}\n")
                self.results_display.append("="*40 + "\n")
        else:
            self.results_display.append("No results found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
