# esp-idf-sql-camera
Take a picture and save it to SQLite.   
This project use [this](https://components.espressif.com/components/espressif/esp32-camera) Camera Driver.   
<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/0974e419-c154-4f2d-b8d7-15f4989b971c" />
<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/742156d7-68b3-44a7-8708-2436894af888" />

We can view the picture saved in SQLite using DB Browser for SQLite.   
DB Browser for SQLite can display JPEG images stored in BLOBs.   
<img width="1180" height="657" alt="Image" src="https://github.com/user-attachments/assets/ffdf6074-02ca-491d-bc0e-fd376fd2ab1d" />

# Hardware requirements
ESP32 development board with OV2640 camera.   
If you use other camera, edit sdkconfig.default.   
From the left:   
- Aithinker ESP32-CAM   
- Freenove ESP32-WROVER CAM   
- UICPAL ESPS3 CAM   
- Freenove ESP32S3-WROVER CAM (Clone)   

![es32-camera](https://github.com/nopnop2002/esp-idf-websocket-camera/assets/6020549/38dbef9a-ed85-4df2-8d22-499b2b497278)

# Software requirements
- ESP-IDF V5.0 or later.   
	ESP-IDF V4.4 release branch reached EOL in July 2024.   

- Python3   
	The ESP32 sends pictures via HTTP.   
	The HTTP server runs on Python.   

- SQLite   
	You can download from [here](https://www.sqlite.org/).   

# Installation
For AiThinker ESP32-CAM, you need to use a USB-TTL converter and connect GPIO0 to GND.   

|ESP-32|USB-TTL|
|:-:|:-:|
|U0TXD|RXD|
|U0RXD|TXD|
|GPIO0|GND|
|5V|5V|
|GND|GND|


```
git clone https://github.com/nopnop2002/esp-idf-sql-camera
cd esp-idf-sql-camera
idf.py set-target {esp32/esp32s3}
idf.py menuconfig
idf.py flash monitor
```

# Start firmware
For AiThinker ESP32-CAM, Change GPIO0 to open and press the RESET button.

# Configuration
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/3d7e2424-13fd-4a60-a916-350ea2f6ed09" />
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/91a20324-2ef2-4ae5-8929-0e52db8647f1" />

### Wifi Setting
Set the information of your access point.   
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/3741e217-a977-447a-8afb-eefde8324c0d" />   
You can connect using the mDNS hostname instead of the IP address.   
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/98f7ed6d-803a-4c1c-80c6-3b2f0c691c82" />   
You can use static IP.   
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/5a4cd92d-b013-4fbb-b356-fc165f05b153" />   

### HTTP Server Setting
The ESP32 sends pictures to the SQLite server via HTTP.   
Specify the IP address and port number of the HTTP server.   
You can use mDNS hostnames instead of IP addresses.   
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/605e813a-4e7d-403e-9ec0-b6da72ba7ccc" />

### Select Board
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/bd8b2cf1-627e-4dd1-b2fb-4c0e5644f5ec" />

### Select Frame Size
Large frame sizes take longer to take a picture.   
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/e242bd93-1518-4203-ab54-70d94aee8571" />

### Select Shutter
ESP32 acts as a HTTP server and listens for requests from HTTP clients.   
You can use this command as shutter.   
`curl -X POST http://{ESP32's IP Address}:8080/post`   
If your ESP32's IP address is `192.168.10.157`, it will look like this.   
`curl -X POST http://192.168.10.157:8080/post`   

In addition to this, you can select the following triggers:   

- Shutter is the Enter key on the keyboard   
	For operation check.   
	When using the USB port provided by the USB Serial/JTAG Controller Console, you need to enable the following line in sdkconfig.
	```
	CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y
	```
	<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/c9704524-dacd-40e1-9805-a93ac862f0ca" />


- Shutter is a GPIO toggle   

	- Initial Sate is PULLDOWN   
	The shutter is prepared when it is turned from OFF to ON, and a picture is taken when it is turned from ON to OFF.   

	- Initial Sate is PULLUP   
	The shutter is prepared when it is turned from ON to OFF, and a picture is taken when it is turned from OFF to ON.   

	I confirmed that the following GPIO can be used.   

	|GPIO|PullDown|PullUp|
	|:-:|:-:|:-:|
	|GPIO12|OK|NG|
	|GPIO13|OK|OK|
	|GPIO14|OK|OK|
	|GPIO15|OK|OK|
	|GPIO16|NG|NG|

	<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/647e88a5-247c-481d-b699-81c8a32d47c1" />

- Shutter is TCP Socket   
	ESP32 acts as a TCP server and listens for requests from TCP clients.   
	You can use tcp_send.py as shutter.   
	`python3 ./tcp_send.py`
	<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/090235e4-ac4b-4027-a9a5-8734a7f6ed5f" />

- Shutter is UDP Socket   
	ESP32 acts as a UDP listener and listens for requests from UDP clients.   
	You can use this command as shutter.   
	`echo -n "take" | socat - UDP-DATAGRAM:255.255.255.255:49876,broadcast`   
	You can use udp_send.py as shutter.   
	Requires netifaces.   
	`python3 ./udp_send.py`   
	<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/88630b59-3211-4156-a644-6c9a777ff502" />   
	You can use these devices as shutters.   
	![Image](https://github.com/user-attachments/assets/cc97da4e-6c06-4604-8362-f81c6fb6eb58)   
	Click [here](https://github.com/nopnop2002/esp-idf-selfie-trigger) for details.   

- Shutter is MQTT Publish   
	ESP32 acts as an MQTT subscriber and listens to requests from MQTT publishes.   
	You can use mosquitto_pub as shutter.   
	`mosquitto_pub -h your_broker -p 1883 -t "/take/picture" -m ""`   
	You can use publish.py as shutter.   
	`python3 ./publish.py`
	<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/4579f229-155e-49f4-afd7-f40c8b660d78" />

### Flash Light   
ESP32-CAM by AI-Thinker have flash light on GPIO4.   
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/a495a9fb-a785-4ed3-99e0-fdc354469d85" />

### PSRAM   
When you use ESP32S3-WROVER CAM, you need to change the PSRAM type.   
![config-psram](https://github.com/nopnop2002/esp-idf-websocket-camera/assets/6020549/ba04f088-c628-46ac-bc5b-2968032753e0)

# Start http server
```
$ python3 http_server.py --help
usage: http_server.py [-h] --path PATH [--port PORT]

options:
  -h, --help   show this help message and exit
  --path PATH  db path
  --port PORT  http port
```

This script creates the `images` table.   
`CREATE TABLE images (id integer primary key autoincrement, date text not null, time text not null, image blob not null)`   
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/bdbda196-ac19-4af4-82ab-9ee9c19c2b55" />   

The ESP32 sends pictures to the SQLite server via HTTP.   
The HTTP server stores pictures in SQLite.   
<img width="659" height="486" alt="Image" src="https://github.com/user-attachments/assets/8cf24fff-c859-41be-bcd0-055336bf6b58" />   

# View picture using Built-in WEB Server
ESP32 works as a web server.   
You can view the pictures taken using the built-in WEB server.   
Enter the ESP32's IP address and port number in the address bar of your browser.   
You can connect using mDNS hostname instead of IP address.   

![browser](https://user-images.githubusercontent.com/6020549/124227364-837a7880-db45-11eb-9d8b-fa15c676adac.jpg)

# View picture using DB Browser for SQLite
This tool runs on Windows, macOS, Linux, and FreeBSD.   
We can download it from [here](https://sqlitebrowser.org/).   
We can view the picture saved in SQLite using it.   
<img width="1180" height="657" alt="Image" src="https://github.com/user-attachments/assets/ffdf6074-02ca-491d-bc0e-fd376fd2ab1d" />

