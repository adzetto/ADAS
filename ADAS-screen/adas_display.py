import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette

class ADASDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADAS Display")
        self.setWindowState(Qt.WindowFullScreen) # Make it full screen
        self.setStyleSheet("background-color: #1a1a1a; color: #e0e0e0;") # Dark theme

        self.stacked_widget = QStackedWidget()
        self.init_ui()

        self.current_mode_index = 0
        self.modes = ["dashboard", "rear_view", "navigation"]
        self.update_display_mode()

        # Simulate data updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulated_data)
        self.timer.start(1000) # Update every 1 second

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Dashboard Mode ---
        self.dashboard_page = QWidget()
        dashboard_layout = QVBoxLayout()
        dashboard_layout.setContentsMargins(20, 20, 20, 20)
        dashboard_layout.setSpacing(10)

        # Top section: Critical Warnings (LDW, BSD)
        top_warning_layout = QHBoxLayout()
        self.ldw_label = QLabel("LDW: OK")
        self.bsd_label = QLabel("BSD: OK")
        self.ldw_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.bsd_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.ldw_label.setAlignment(Qt.AlignCenter)
        self.bsd_label.setAlignment(Qt.AlignCenter)
        top_warning_layout.addWidget(self.ldw_label)
        top_warning_layout.addWidget(self.bsd_label)
        dashboard_layout.addLayout(top_warning_layout)

        # Middle section: Speed (Cruise Control)
        self.speed_label = QLabel("SPEED: 0 km/h")
        self.speed_label.setFont(QFont("Arial", 72, QFont.Bold))
        self.speed_label.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(self.speed_label)

        # Bottom section: TSR, Auto Light
        bottom_info_layout = QHBoxLayout()
        self.tsr_label = QLabel("TSR: No Sign")
        self.auto_light_label = QLabel("Auto Light: OFF")
        self.tsr_label.setFont(QFont("Arial", 24))
        self.auto_light_label.setFont(QFont("Arial", 24))
        self.tsr_label.setAlignment(Qt.AlignCenter)
        self.auto_light_label.setAlignment(Qt.AlignCenter)
        bottom_info_layout.addWidget(self.tsr_label)
        bottom_info_layout.addWidget(self.auto_light_label)
        dashboard_layout.addLayout(bottom_info_layout)

        self.dashboard_page.setLayout(dashboard_layout)
        self.stacked_widget.addWidget(self.dashboard_page) # Index 0

        # --- Rear View Camera Mode ---
        self.rear_view_page = QWidget()
        rear_view_layout = QVBoxLayout()
        self.rear_view_label = QLabel("REAR VIEW CAMERA FEED")
        self.rear_view_label.setFont(QFont("Arial", 48, QFont.Bold))
        self.rear_view_label.setAlignment(Qt.AlignCenter)
        rear_view_layout.addWidget(self.rear_view_label)
        self.rear_view_page.setLayout(rear_view_layout)
        self.stacked_widget.addWidget(self.rear_view_page) # Index 1

        # --- Navigation Mode ---
        self.navigation_page = QWidget()
        navigation_layout = QVBoxLayout()
        self.navigation_label = QLabel("RACE NAVIGATION MAP")
        self.navigation_label.setFont(QFont("Arial", 48, QFont.Bold))
        self.navigation_label.setAlignment(Qt.AlignCenter)
        self.lap_counter_label = QLabel("LAP: 0/0")
        self.lap_counter_label.setFont(QFont("Arial", 36))
        self.lap_counter_label.setAlignment(Qt.AlignCenter)
        navigation_layout.addWidget(self.navigation_label)
        navigation_layout.addWidget(self.lap_counter_label)
        self.navigation_page.setLayout(navigation_layout)
        self.stacked_widget.addWidget(self.navigation_page) # Index 2

        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def update_display_mode(self):
        self.stacked_widget.setCurrentIndex(self.current_mode_index)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right: # Simulate "Forward" button
            self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
            self.update_display_mode()
        elif event.key() == Qt.Key_Left: # Simulate "Backward" button
            self.current_mode_index = (self.current_mode_index - 1 + len(self.modes)) % len(self.modes)
            self.update_display_mode()
        elif event.key() == Qt.Key_Q: # Quit
            self.close()

    def update_simulated_data(self):
        # Simulate LDW/BSD warnings
        if self.current_mode_index == 0: # Only update dashboard elements in dashboard mode
            import random
            if random.random() < 0.1: # 10% chance of warning
                self.ldw_label.setText("LDW: WARNING!")
                self.ldw_label.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.ldw_label.setText("LDW: OK")
                self.ldw_label.setStyleSheet("color: #e0e0e0;")

            if random.random() < 0.05: # 5% chance of BSD warning
                self.bsd_label.setText("BSD: OBJECT!")
                self.bsd_label.setStyleSheet("color: orange; font-weight: bold;")
            else:
                self.bsd_label.setText("BSD: OK")
                self.bsd_label.setStyleSheet("color: #e0e0e0;")

            # Simulate speed (Cruise Control)
            current_speed = random.randint(60, 120)
            self.speed_label.setText(f"SPEED: {current_speed} km/h")

            # Simulate TSR
            signs = ["No Sign", "Speed 50", "Stop Sign", "Yield"]
            self.tsr_label.setText(f"TSR: {random.choice(signs)}")

            # Simulate Auto Light
            light_status = "ON" if random.random() < 0.5 else "OFF"
            self.auto_light_label.setText(f"Auto Light: {light_status}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    adas_display = ADASDisplay()
    adas_display.show()
    sys.exit(app.exec_())
