# CWC - Chat With Computer

Welcome to **Chat With Computer (CWC)**! This innovative application allows users to have engaging conversations with their computer, providing customizable interaction styles and detailed system information. 

## Overview

**Chat With Computer (CWC)** is a versatile tool designed to interact with your PC through a user-friendly chat interface. Key features include customizable chat styles, multiple language options, and detailed hardware information. The application also offers a unique "Controller Mode" for executing commands directly from the chat window.

## Features

- **Interactive Chat Interface:** Engage in dynamic conversations with your computer.
- **Customizable Styles:** Choose from predefined styles or create your own for a personalized experience.
- **Multi-language Support:** Select from various languages to enhance communication.
- **Controller Mode:** Execute system commands directly from the chat interface when enabled.
- **Detailed System Information:** Access comprehensive details about your computer’s hardware and software.

## Installation

### Pre-Built Binaries

For Linux users, a pre-built version of the application is available for free. You can download it from the [Releases](https://github.com/retrotee/CWC-Chat-With-Computer/releases) tab.

### Building from Source

If you prefer to build the application from source, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/retrotee/CWC-Chat-With-Computer.git
   cd CWC-Chat-With-Computer
   ```

2. **Install Dependencies:**
   Ensure you have the following Python packages installed:
   - `PyQt5`
   - `GPUtil`
   - `psutil`
   - `cpuinfo`
   - `g4f`
   - `curl_cffi`

   You can install these using pip:
   ```bash
   pip install PyQt5 GPUtil psutil py-cpuinfo g4f curl_cffi
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```

## Usage

### Permissions and Restrictions

You are allowed to:

- **Use** the application freely for personal purposes only.
- **Enhance** and modify the application. When doing so, please credit the original authors.

You are prohibited from:

- **Selling** the application or any of its derived versions.
- **Removing** or omitting credits to the original developers.
- **Closing the Source**: Any distributed versions of the code must remain open source.
- **Malicious Use**: Do not use the software for harmful purposes or malware.
- **Exploitative Technology**: Avoid using the application or its code to exploit or harm others.

### Credits

Special thanks to the following contributors and libraries that made this project possible:

- **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)** - GUI framework by Riverbank Computing.
- **[GPUtil](https://github.com/anderskm/gputil/)** - For GPU information, created by Anders Krogh Mortensen.
- **[psutil](https://github.com/giampaolo/psutil)** - System utilities library by Giampaolo Rodola.
- **[cpuinfo](https://github.com/workhorsy/py-cpuinfo)** - CPU information library by Matthew Jones.
- **[g4f](https://github.com/xtekky/gpt4free)** - AI interaction client by Tekky.
- **[curl_cffi](https://github.com/lexiforest/curl_cffi)** - Python binding for curl-impersonate via cffi by Lyonnet.

## License

This project is licensed under the [GPL License](LICENSE). See the `LICENSE` file for details.

## Thank you!

Thank you for using **Chat With Computer (CWC)**. We hope you find it both useful and enjoyable!

---

Happy coding!
