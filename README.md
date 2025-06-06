# GoPro Proxy Tool for DaVinci Resolve

![GoPro Proxy Tool Screenshot](<img width="517" alt="image" src="https://github.com/user-attachments/assets/74b69551-ac5d-4059-a9c8-8950ffc08d21" />
)

A simple, modern, and efficient desktop application designed to streamline the proxy workflow for GoPro users editing in DaVinci Resolve. This tool automates the tedious process of converting GoPro's low-resolution `.LRV` files into usable proxies that DaVinci Resolve can link to your high-resolution source footage.

Built with Python and CustomTkinter, it features a clean, dark-themed interface with drag-and-drop support.

---

## The Problem It Solves

GoPro cameras create low-resolution video files (`.LRV`) alongside your main high-resolution `.MP4` files. These are perfect for use as editing proxies, but they aren't in a format that DaVinci Resolve can immediately use. To make them work, you need to:
1.  Rename the file extension from `.LRV` to `.MP4`.
2.  Change the file prefix from `GL` (GoPro Low) to `GX` to match the high-resolution source file.
3.  Organize them into a separate `proxy` folder.

This tool automates all three steps with a single click.

## Key Features

- **Automated Batch Processing**: Convert hundreds of files at once.
- **Drag & Drop**: Simply drag your `.LRV` files onto the application window.
- **Correct Naming Convention**: Automatically renames `GL...LRV` files to `GX...MP4`.
- **Smart Folder Organization**: Creates a `proxy` subfolder in the same directory as your source footage and moves the renamed files there, keeping your project tidy.
- **Modern UI**: A clean, dark, and user-friendly interface.
- **Cross-Platform**: Built with Python, it can be compiled for Windows, macOS, and Linux.

## Getting Started (For Users)

The easiest way to get the app is to download the latest pre-compiled version.

1.  Go to the [**Releases Page**](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/releases) of this repository.
2.  Download the `.zip` file for your operating system (e.g., `GoProProxyTool-windows-v1.0.zip`).
3.  Unzip the file and run the `GoProProxyTool.exe` executable.

## How to Use

1.  **Launch the application.**
2.  **Add Files**: Drag and drop your `.LRV` files directly into the application window, or use the `Browse Files` button to select them.
3.  **Process**: Click the `Process Files` button. The app will rename the files and move them to a newly created `proxy` folder.
4.  **Link in DaVinci Resolve**:
    - Import your original high-resolution `GX...MP4` files into your DaVinci Resolve project.
    - In the Media Pool, select the clips you want to link.
    - Right-click and choose **"Link Proxy Media..."**.
    - Navigate to the `proxy` folder and select the corresponding proxy files. DaVinci Resolve will handle the rest!

## Building From Source (For Developers)

If you want to build the application yourself, follow these steps.

**Prerequisites:**
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

**Instructions:**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd YOUR_REPOSITORY
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

5.  **Build the executable:**
    To create a standalone `.exe` file, use PyInstaller.
    ```bash
    # Install PyInstaller if you haven't already
    pip install pyinstaller

    # Run the build command
    pyinstaller --name="GoProProxyTool" --noconsole --onefile --icon="assets/icon.ico" --collect-all customtkinter --collect-all tkinterdnd2 main.py
    ```
    The final executable will be located in the `dist` folder.

## Technology Stack

- **Language**: Python
- **GUI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Drag & Drop**: [tkinterdnd2-universal](https://github.com/akai-katto/tkinterdnd2-universal)
- **Bundler**: [PyInstaller](https://pyinstaller.org/)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
