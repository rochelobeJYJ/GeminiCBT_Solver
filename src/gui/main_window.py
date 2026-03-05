import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QCheckBox,
                             QLineEdit, QTextBrowser, QApplication,
                             QProgressBar, QSizePolicy, QMessageBox, QGroupBox)

from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize, QRect
from PyQt6.QtGui import QAction, QPainter, QColor, QPen

from src.utils import ConfigManager
from src.gemini_client import GeminiSolver
from src.gui.snipping_tool import SnippingTool
from src.gui.dialogs import ApiKeyDialog, DEFAULT_MODEL

import tempfile

class OverlayIndicator(QWidget):
    """
    A transparent, click-through overlay showing red brackets at corners.
    """
    def __init__(self, rect: QRect = None):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.padding = 4
        self.corner_length = 15
        self.line_width = 3
        self.color = QColor(255, 0, 0) # Red
        
        if rect:
            self.update_rect(rect)

    def update_rect(self, rect: QRect):
        # Expand geometry slightly to draw outside the content
        geo = rect.adjusted(-self.padding, -self.padding, self.padding, self.padding)
        self.setGeometry(geo)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pen = QPen(self.color, self.line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap) # Round ends
        painter.setPen(pen)
        
        w = self.width()
        h = self.height()
        l = self.corner_length
        
        # Top-Left (ㄱ)
        painter.drawLine(0, 0, l, 0)
        painter.drawLine(0, 0, 0, l)

        # Top-Right (reversed ㄱ)
        painter.drawLine(w, 0, w - l, 0)
        painter.drawLine(w, 0, w, l)

        # Bottom-Left (ㄴ)
        painter.drawLine(0, h, l, h)
        painter.drawLine(0, h, 0, h - l)

        # Bottom-Right (reversed ㄴ)
        painter.drawLine(w, h, w - l, h)
        painter.drawLine(w, h, w, h - l)

class SolverWorker(QThread):
    chunk_received = pyqtSignal(str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, solver, image_path, context):
        super().__init__()
        self.solver = solver
        self.image_path = image_path
        self.context = context
        self.running = True

    def run(self):
        try:
            stream_gen = self.solver.solve_problem_stream(self.image_path, self.context)
            for chunk_text in stream_gen:
                if not self.running:
                    break
                self.chunk_received.emit(chunk_text)
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))
    
    def stop(self):
        self.running = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CBT Solver")
        # Reduced size: 360x480 (80% of 450x600)
        self.resize(360, 480)
        self.setMinimumSize(320, 400)
        
        self._apply_styles()
        
        self.config_manager = ConfigManager()
        self.api_key = None
        self.current_model = DEFAULT_MODEL
        self.solver = None
        self.snipping_tool = None
        
        self.current_capture_rect = None
        self.solver_thread = None
        self.overlay_indicator = None
        
        self._setup_ui()
        QTimer.singleShot(100, self._check_api_key)

    def _apply_styles(self):
        # Reduced font sizes: 14px -> 12px, margin adjustments
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F2F5;
            }
            QWidget {
                font-family: 'Malgun Gothic', sans-serif;
                font-size: 12px;
                color: #333333;
            }
            QGroupBox {
                background-color: #FFFFFF;
                border: 1px solid #D0D0D0;
                border-radius: 5px;
                margin-top: 18px;
                font-weight: bold;
                color: #555555;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
                left: 8px;
                color: #007ACC;
            }
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 4px;
                background-color: #FFFFFF;
            }
            QLineEdit:focus {
                border: 1px solid #007ACC;
            }
            QTextBrowser {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
                font-size: 12px;
                line-height: 1.4;
            }
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 4px 10px;
                min-height: 22px;
            }
            QPushButton:hover {
                background-color: #E6F7FF;
                border: 1px solid #007ACC;
                color: #007ACC;
            }
            QPushButton#ActionBtn {
                background-color: #007ACC;
                color: white;
                border: none;
                font-weight: bold;
                padding: 6px 14px;
            }
            QPushButton#ActionBtn:hover {
                background-color: #005A9E;
            }
            QCheckBox {
                spacing: 4px;
            }
            QProgressBar {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: #FFFFFF;
                height: 5px;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
            }
        """)

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)
        
        # --- Top Control Panel ---
        top_group = QGroupBox("설정")
        top_layout = QVBoxLayout()
        top_layout.setSpacing(6)
        top_layout.setContentsMargins(8, 12, 8, 8)
        
        # Row 1
        row1 = QHBoxLayout()
        self.ontop_chk = QCheckBox("항상 위")
        self.ontop_chk.toggled.connect(self.toggle_always_on_top)
        
        self.indicator_chk = QCheckBox("영역 표시")
        self.indicator_chk.setChecked(True)
        self.indicator_chk.toggled.connect(self.toggle_overlay)
        
        settings_btn = QPushButton("API 설정")
        settings_btn.clicked.connect(self.open_settings)
        
        row1.addWidget(self.ontop_chk)
        row1.addWidget(self.indicator_chk)
        row1.addStretch()
        row1.addWidget(settings_btn)
        
        # Row 2
        row2 = QHBoxLayout()
        lbl = QLabel("과목:")
        self.context_input = QLineEdit()
        self.context_input.setPlaceholderText("예: 정보처리기사")
        row2.addWidget(lbl)
        row2.addWidget(self.context_input)
        
        top_layout.addLayout(row1)
        top_layout.addLayout(row2)
        top_group.setLayout(top_layout)
        
        main_layout.addWidget(top_group)
        
        # --- Actions Group ---
        action_group = QGroupBox("실행")
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(8, 12, 8, 8)
        
        self.btn_select_area = QPushButton("영역 지정")
        self.btn_select_area.clicked.connect(self.start_selection_mode)
        
        self.btn_capture_solve = QPushButton("풀이 실행")
        self.btn_capture_solve.setObjectName("ActionBtn")
        self.btn_capture_solve.clicked.connect(self.capture_and_solve)
        
        action_layout.addWidget(self.btn_select_area)
        action_layout.addWidget(self.btn_capture_solve)
        action_group.setLayout(action_layout)
        
        main_layout.addWidget(action_group)
        
        # --- Result Area ---
        result_group = QGroupBox("결과")
        result_layout = QVBoxLayout()
        result_layout.setContentsMargins(8, 12, 8, 8)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        
        self.status_msg = QLabel("준비")
        self.status_msg.setStyleSheet("color: #666; font-size: 11px;")
        
        self.result_browser = QTextBrowser()
        
        result_layout.addWidget(self.progress_bar)
        result_layout.addWidget(self.status_msg)
        result_layout.addWidget(self.result_browser)
        result_group.setLayout(result_layout)
        
        main_layout.addWidget(result_group, stretch=1)
        
        central_widget.setLayout(main_layout)

    def _check_api_key(self):
        key = self.config_manager.load_api_key()
        saved_model = self.config_manager.load_model()
        if saved_model:
            self.current_model = saved_model
        if key:
            self.api_key = key
            self._init_solver()
        else:
            self.open_settings()

    def _init_solver(self):
        if self.api_key:
            try:
                self.solver = GeminiSolver(self.api_key, model_name=self.current_model)
                self.status_msg.setText(f"준비 (모델: {self.current_model})")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"API 초기화 실패: {e}")

    def open_settings(self):
        dialog = ApiKeyDialog(self, current_model=self.current_model)
        if hasattr(self, 'api_key') and self.api_key:
            dialog.key_input.setText(self.api_key)
        if dialog.exec():
            new_key = dialog.get_key()
            if new_key:
                self.config_manager.save_api_key(new_key)
                self.api_key = new_key
            # Save model regardless
            new_model = dialog.get_model()
            if new_model:
                self.current_model = new_model
                self.config_manager.save_model(new_model)
            self._init_solver()

    def toggle_always_on_top(self, checked):
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()

    def toggle_overlay(self, checked):
        if self.overlay_indicator:
            if checked and self.current_capture_rect:
                self.overlay_indicator.show()
                self.overlay_indicator.update_rect(self.current_capture_rect)
            else:
                self.overlay_indicator.hide()

    def start_selection_mode(self):
        # 1. Robust Cleanup of Overlay
        if self.overlay_indicator:
            self.overlay_indicator.close()
            self.overlay_indicator.deleteLater()
            self.overlay_indicator = None
        
        # 2. Cleanup previous SnippingTool (important to avoid ghost windows)
        if self.snipping_tool:
            self.snipping_tool.close()
            self.snipping_tool.deleteLater()
            self.snipping_tool = None

        # 3. Create new SnippingTool
        self.snipping_tool = SnippingTool()
        self.snipping_tool.area_selected.connect(self.handle_selection)
        self.snipping_tool.canceled.connect(self.handle_selection_params_cancel)
        
        self.hide()
        # Give Qt event loop a moment to process the cleanup and hiding
        QTimer.singleShot(250, self.snipping_tool.show)

    def handle_selection(self, rect):
        self.current_capture_rect = rect
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized)
        self.activateWindow()
        self.status_msg.setText(f"영역: {rect.width()}x{rect.height()}")
        
        if self.overlay_indicator:
            self.overlay_indicator.close()
        
        self.overlay_indicator = OverlayIndicator(rect)
        if self.indicator_chk.isChecked():
            self.overlay_indicator.show()
        else:
            self.overlay_indicator.hide()

    def handle_selection_params_cancel(self):
        self.show()
        self.activateWindow()

    def closeEvent(self, event):
        if self.overlay_indicator:
            self.overlay_indicator.close()
        event.accept()

    def capture_and_solve(self):
        if not self.solver:
            QMessageBox.warning(self, "경고", "먼저 API Key를 설정해주세요.")
            self.open_settings()
            return

        if not self.current_capture_rect:
            QMessageBox.information(self, "안내", "먼저 '영역 지정'을 해주세요.")
            self.start_selection_mode()
            return
            
        self.btn_capture_solve.setEnabled(False)
        self.btn_select_area.setEnabled(False)
        self.result_browser.clear()
        self.progress_bar.setVisible(True)
        self.status_msg.setText("분석 중...")
        
        self.hide()
        if self.overlay_indicator:
            self.overlay_indicator.hide()
            
        QTimer.singleShot(150, self._perform_capture_and_process)

    def _perform_capture_and_process(self):
        try:
            screen = QApplication.primaryScreen()
            if not screen: return

            rect = self.current_capture_rect
            pixmap = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
            
            self.show()
            self.activateWindow()
            if self.overlay_indicator and self.indicator_chk.isChecked():
                self.overlay_indicator.show()
            
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                pixmap.save(f.name)
                temp_path = f.name
            
            context = self.context_input.text()
            
            self.solver_thread = SolverWorker(self.solver, temp_path, context)
            self.solver_thread.chunk_received.connect(self.append_result_chunk)
            self.solver_thread.finished_signal.connect(self.on_solve_finished)
            self.solver_thread.error_signal.connect(self.on_solve_error)
            self.solver_thread.start()
            
        except Exception as e:
            self.show()
            if self.overlay_indicator and self.indicator_chk.isChecked():
                self.overlay_indicator.show()
            self.on_solve_error(f"실패: {str(e)}")

    def append_result_chunk(self, text):
        cursor = self.result_browser.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.result_browser.setTextCursor(cursor)
        self.result_browser.insertPlainText(text)
        sb = self.result_browser.verticalScrollBar()
        sb.setValue(sb.maximum())

    def on_solve_finished(self):
        self.progress_bar.setVisible(False)
        self.status_msg.setText("완료")
        self.btn_capture_solve.setEnabled(True)
        self.btn_select_area.setEnabled(True)
        
        final_text = self.result_browser.toPlainText()
        self.result_browser.setMarkdown(final_text)

    def on_solve_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.status_msg.setText("오류")
        self.result_browser.setText(f"⛔ {error_msg}")
        self.btn_capture_solve.setEnabled(True)
        self.btn_select_area.setEnabled(True)
