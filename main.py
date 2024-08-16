import sys
import GPUtil
import platform
import psutil
import cpuinfo
import os
import subprocess
import getpass
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
                             QComboBox, QCheckBox, QLabel, QLineEdit)
from PyQt5.QtGui import QFont, QPalette, QColor, QTextCharFormat, QBrush, QSyntaxHighlighter
from PyQt5.QtCore import Qt, QRegExp
from g4f.client import Client
from g4f.Provider import You


class MarkdownHighlighter(QSyntaxHighlighter):
    """Class to handle Markdown syntax highlighting in QTextEdit."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Define highlighting rules
        self._add_highlighting_rule(r"^#+ .*", QFont.Bold, QColor("#58A6FF"))  # Heading
        self._add_highlighting_rule(r"\*\*.*\*\*", QFont.Bold, QColor())  # Bold
        self._add_highlighting_rule(r"\*.*\*", QFont.StyleItalic, QColor())  # Italic
        self._add_highlighting_rule(r"`.*`", QFont("Courier"), QColor("#2C3E50"))  # Code
        self._add_highlighting_rule(r"\[.*\]\(.*\)", QFont(), QColor("#58A6FF"), underline=True)  # Link

    def _add_highlighting_rule(self, pattern, font_weight, color, underline=False):
        """Add a highlighting rule."""
        fmt = QTextCharFormat()
        fmt.setFontWeight(font_weight)
        fmt.setForeground(color)
        if underline:
            fmt.setFontUnderline(True)
        self.highlighting_rules.append((QRegExp(pattern), fmt))

    def highlightBlock(self, text):
        """Apply highlighting rules to each block of text."""
        for pattern, fmt in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)


class CWC(QMainWindow):
    """Main window class for the Chat With Computer application."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CWC - Chat With Computer")
        self.setGeometry(100, 100, 800, 600)

        # Set up the main layout
        self._setup_layout()

        # Initialize chat history
        self.history = []

        # Set up dark theme
        self.set_dark_theme()

    def _setup_layout(self):
        """Set up the layout for the main window."""
        main_layout = QHBoxLayout()

        # Create and set up the sidebar
        sidebar = self._create_sidebar()
        main_layout.addWidget(sidebar)

        # Create and set up the chat area
        chat_widget = self._create_chat_widget()
        main_layout.addWidget(chat_widget)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _create_sidebar(self):
        """Create and return the sidebar widget."""
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout()

        # Add title and subtitle
        sidebar_layout.addWidget(self._create_label("CWC", 16, QFont.Bold))
        sidebar_layout.addWidget(self._create_label("Chat With Computer"))

        sidebar_layout.addSpacing(20)

        # Add language selection
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Spanish", "French", "German", "Chinese", "Japanese"])
        sidebar_layout.addWidget(QLabel("Choose Language:"))
        sidebar_layout.addWidget(self.lang_combo)

        # Add style selection
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Professional", "Humorous", "2 word answer", "Custom"])
        sidebar_layout.addWidget(QLabel("Select Style:"))
        sidebar_layout.addWidget(self.style_combo)

        # Add custom style input
        self.custom_style_input = QLineEdit()
        self.custom_style_input.setPlaceholderText("Enter custom style")
        self.custom_style_input.hide()
        sidebar_layout.addWidget(self.custom_style_input)

        # Connect style combo box to show/hide custom style input
        self.style_combo.currentTextChanged.connect(self.toggle_custom_style)

        # Add controller mode checkbox
        self.controller_mode = QCheckBox("Controller Mode")
        sidebar_layout.addWidget(self.controller_mode)

        # Add clear chat button
        clear_button = QPushButton("Clear Chat")
        clear_button.clicked.connect(self.clear_chat)
        sidebar_layout.addWidget(clear_button)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        return sidebar

    def _create_label(self, text, font_size=12, font_weight=QFont.Normal):
        """Create a QLabel with specified text and font settings."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", font_size, font_weight))
        return label

    def _create_chat_widget(self):
        """Create and return the chat widget."""
        chat_widget = QWidget()
        chat_layout = QVBoxLayout()

        # Create chat history area
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        font = QFont("Courier")
        font.setStyleHint(QFont.Monospace)
        self.chat_history.setFont(font)
        self.chat_history.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
            }
        """)
        chat_layout.addWidget(self.chat_history)

        # Create user input area
        self.user_input = QTextEdit()
        self.user_input.setFixedHeight(50)
        self.user_input.installEventFilter(self)
        chat_layout.addWidget(self.user_input)

        # Add send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        chat_layout.addWidget(send_button)

        chat_widget.setLayout(chat_layout)
        return chat_widget

    def set_dark_theme(self):
        """Set the application theme to dark mode."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

    def toggle_custom_style(self, style):
        """Show or hide the custom style input based on the selected style."""
        self.custom_style_input.setVisible(style == "Custom")

    def send_message(self):
        """Send the user's message and display the response."""
        user_input = self.user_input.toPlainText()
        if user_input:
            self.append_message("User", user_input, QColor("#FF6B6B"))
            response = self.get_ai_response(user_input)
            self.append_message("PC", response, QColor("#4ECDC4"))
            self.user_input.clear()

    def append_message(self, sender, message, color):
        """Append a message to the chat history."""
        sender_color = color.name()
        wrapped_message = self.wrap_text(message, 60)  # Wrap at 60 characters

        html = f"""
        <table style="width:100%; border-collapse: collapse;">
            <tr>
                <td style="width: 100px; color: {sender_color}; vertical-align: top; padding-right: 10px;">
                    <pre style="margin: 0;">{sender:12}</pre>
                </td>
                <td style="color: #ffffff;">
                    <pre style="margin: 0; white-space: pre-wrap;">{wrapped_message}</pre>
                </td>
            </tr>
        </table>
        """

        self.chat_history.append(html)
        self.chat_history.ensureCursorVisible()

    def wrap_text(self, text, width):
        """Wrap text to the specified width."""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            if len(' '.join(current_line + [word])) <= width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)

    def get_ai_response(self, user_input):
        """Get a response from the AI based on user input."""
        pc_details = self.get_pc_details()
        lang = self.lang_combo.currentText()
        style = self.style_combo.currentText()
        custom_style = self.custom_style_input.text() if style == "Custom" else style
        controller_mode = self.controller_mode.isChecked()

        prompt = f"""
        Hello! You are a PC that loves to engage users in a {custom_style.lower()} style. You enjoy sharing your technical details. Your personality shines through as you answer in short sentences.

        Please note:
        - If Controller Mode is enabled, execute commands (bash or cmd depending on the OS) enclosed in triple backticks (```) and provide feedback or errors. You can also commend or teach the user while executing the command.
        - If Controller Mode is disabled, do not attempt to execute any commands and provide the response in a conversational style.
        - Do not include the command in your response text.
        - Do not include the programming language's name in the triple backticks.
        - Do not use markdown except when the user asks for it or you need to execute commands (Controller Mode).

        Controller Mode: {controller_mode}

        Your task is to respond to user input in a friendly and engaging way while referencing prior chat history. If there is any chat history, please respond ONLY to the last one (so you don't need to say 'Hi' every time). Importantly, avoid giving any help or assistance unless the user explicitly requests it.

        Here are the specifics you'll need to incorporate when responding:
        - Please use the following language: {lang}
        - Here are some details about you:
          {pc_details}

        And here is the user input: {user_input}

        This is the chat history with the user: {self.history}
        """

        client = Client(provider=You)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        ai_response = response.choices[0].message.content

        if controller_mode and '```' in ai_response:
            command = ai_response.split('```')[1].strip()
            self.append_message("Command", f" {command}", QColor("#FFA500"))  # Orange color for Command
            self.run_command_in_terminal(command)

            # Remove the command from the AI response
            ai_response = ai_response.split('```')[0] + ai_response.split('```')[2]

        self.history.append({"user": user_input, "pc": ai_response})

        return ai_response

    def get_pc_details(self):
        """Retrieve detailed information about the PC."""
        details = {
            "name": platform.node(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": cpuinfo.get_cpu_info()['brand_raw'],
            "ram": f"{str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + ' GB'}",
            "gpu": GPUtil.getGPUs()[0].name if GPUtil.getGPUs() else "No GPU detected",
            "motherboard": self.get_motherboard_name(),
            "space_total": f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB",
            "space_used": f"{psutil.disk_usage('/').used / (1024 ** 3): .2f} GB",
            "space_free": f"{psutil.disk_usage('/').free / (1024 ** 3): .2f} GB",
            "uname": platform.uname(),
        }
        return details

    def get_motherboard_name(self):
        """Retrieve the motherboard name."""
        try:
            if os.name == 'nt':  # Windows
                motherboard_info = \
                subprocess.check_output("wmic baseboard get product", shell=True).decode().strip().split('\n')[
                    1].strip()
            elif os.name == 'posix':  # Linux
                motherboard_info = subprocess.check_output("sudo dmidecode -t baseboard | grep 'Product Name'",
                                                           shell=True).decode().strip()
                motherboard_info = motherboard_info.split(': ')[1]
            else:
                return "Operating system not supported."
            return motherboard_info
        except subprocess.CalledProcessError:
            return "Error retrieving motherboard name."

    def run_command_in_terminal(self, command):
        """Run a command in the terminal based on the operating system."""
        if platform.system() == "Windows":
            subprocess.Popen(f'start cmd /K "{command}"', shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(['osascript', '-e', f'tell app "Terminal" to do script "{command}"'])
        else:  # Linux
            subprocess.Popen(['x-terminal-emulator', '-e', f'bash -c "{command}; read -p \'Press Enter to exit\'"'])

    def clear_chat(self):
        """Clear the chat history."""
        self.chat_history.clear()
        self.history = []

    def eventFilter(self, obj, event):
        """Handle events for the user input text area."""
        if obj is self.user_input and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return and event.modifiers() != Qt.ShiftModifier:
                self.send_message()
                return True
            elif event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
                cursor = self.user_input.textCursor()
                cursor.insertText("\n")
                return True
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cwc = CWC()
    cwc.show()
    sys.exit(app.exec_())
