import sys
import pandas as pd
import pytz
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class StockPlotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Remaining Plotter")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input_layout = QHBoxLayout()
        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Enter Product Name")
        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("Enter Stock")
        self.input_layout.addWidget(QLabel("Product:"))
        self.input_layout.addWidget(self.product_input)
        self.input_layout.addWidget(QLabel("Stock:"))
        self.input_layout.addWidget(self.stock_input)

        self.layout.addLayout(self.input_layout)

        self.plot_button = QPushButton("Generate Plot")
        self.plot_button.clicked.connect(self.generate_plot)
        self.layout.addWidget(self.plot_button)

        self.figure = Figure(facecolor='#121212')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def generate_plot(self):
        product = self.product_input.text()
        try:
            stock = int(self.stock_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Stock must be an integer.")
            return

        try:
            data = pd.read_csv("data.csv")
            data = data[data['ProductName'] == product]
            data = data.drop(columns=['ProductVersionType', 'TransactionType', 'TransactionAmount',
                                      'Grade', 'VendingOutletName', 'AuthorizationSource'])

            data['TransactionDateTimeUTC'] = pd.to_datetime(data['TransactionDateTimeUTC'], errors='coerce', utc=True)
            data = data.dropna(subset=['TransactionDateTimeUTC'])
            data['TransactionDateTimeTokyo'] = data['TransactionDateTimeUTC'].dt.tz_convert('Asia/Tokyo')

            data['Date'] = data['TransactionDateTimeTokyo'].dt.date
            data['Hour'] = data['TransactionDateTimeTokyo'].dt.hour

            dhourly_counts = data.groupby(['Date', 'Hour']).size().reset_index(name='HourlyCount')
            dhourly_counts['CumulativeBLTs'] = dhourly_counts.groupby('Date')['HourlyCount'].cumsum()
            dhourly_counts['Date'] = pd.to_datetime(dhourly_counts['Date'])
            dhourly_counts = dhourly_counts[dhourly_counts['Date'].dt.year == 2024]

            filtered = dhourly_counts[(dhourly_counts['Hour'] >= 8) & (dhourly_counts['Hour'] <= 15)]
            pivot = filtered.pivot(index='Date', columns='Hour', values='CumulativeBLTs')
            pivot = pivot.reindex(columns=range(8, 16), fill_value=0)
            pivot = pivot.ffill(axis=1).fillna(0)

            blt_lists = pivot.values.tolist()
            data_per_day = list(zip(pivot.index.strftime('%Y-%m-%d'), blt_lists))

            for i in range(len(data_per_day)):
                for j in range(8):
                    data_per_day[i][1][j] = stock - data_per_day[i][1][j]

            av_data = [0] * 8
            for j in range(8):
                total = sum(day[1][j] for day in data_per_day)
                av_data[j] = total / len(data_per_day)

            self.plot(av_data, product)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def plot(self, data, product):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)

        hours = list(range(8, 16))
        ax.plot(hours, data, marker='o', linestyle='-', color='#FFD700', linewidth=2)

        ax.set_title(f"Stock Remaining by Hour: {product}", fontsize=14, color='#FFD700')
        ax.set_xlabel("Hour", fontsize=12, color='#FFD700')
        ax.set_ylabel("Stock Remaining", fontsize=12, color='#FFD700')
        ax.set_xticks(hours)
        ax.grid(True, linestyle='--', color='#B8860B', alpha=0.3)

        ax.set_facecolor('#121212')
        for spine in ax.spines.values():
            spine.set_color('#FFD700')

        ax.tick_params(axis='x', colors='#FFD700')
        ax.tick_params(axis='y', colors='#FFD700')

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockPlotApp()
    window.show()
    sys.exit(app.exec_())
