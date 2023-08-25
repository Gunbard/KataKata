# KataKata
Simple inventory/catalog management system for collecting crap mostly based around UPCs

![KataKata screenshot](/readme-img/screenshot-1.0.0.png)

### Features
- Automatic UPC data lookup and scraping
- Data is saved locally, including images
- Extremely portable

### Sample workflow I use
- Connect a cheap barcode scanner to phone
- Scan UPCs/barcodes to a text editor app, one per line
- Save as a .txt file and share directly to Google Drive
- Import into KataKata and save as a new catalog (PS1 games, Nendoroids, etc.)
- Refresh All and repeat if UPC data source times out

Keep catalog .json files in Google Drive for easy access and backup.

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
pyuic5 mainWindow.ui -o mainWindow.py; pyuic5 refreshDialog.ui -o refreshDialog.py
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

### TODO
- [ ] Generate an HTML report
- [ ] Searching/filtering
- [ ] Multithread instead of locking up the UI when refreshing
- [ ] Date added/acquired field
- [ ] Recent catalogs list
- [ ] Custom/multiple UPC data sources instead of being a jerk and scraping public database sites
- [ ] Make an icon
