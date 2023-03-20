# KataKata
Simple inventory/catalog management system for collecting crap

![KataKata screenshot](/readme-img/screenshot-1.0.0.png)

### Download/Pre-built Binaries
See [Releases](https://github.com/Gunbard/KataKata/releases)

##### Tested with Python 3.8.6/venv on Windows 10

## Local Development

### Install Dependencies
```sh
pip install -r requirements.in
```

### (Re)compiling the UI
```sh
pyuic5 mainWindow.ui -o mainWindow.py
```

### Running
```sh
python main.py
```

### Building standalone executable
```sh
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
```

Built exe will be in 'dist' folder