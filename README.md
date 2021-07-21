# Air-Detect-for-RespberryPi3

Raspberry Pi建置步驟\
Prepare: Respberry Pi 3, CJMCU-8128\
一、基本設定\
1.燒錄raspberry-pi-desktop至SD卡\
2.加入空白ssh的檔案(所有檔案*.*)至SD卡\
3.退出SD卡，插入Raspberry Pi，並替Raspberry Pi接上網路線\
4.掃描區域網路，尋找到Raspberry Pi Foundation裝置，利用此IP遠端進入Raspberry Pi\
5.預設使用者名稱為：pi，預設密碼為：raspberry\
6.進入 sudo raspi-config 設定密碼(Change User Password)、名稱(Hostname)\
7.進入 Localisation Options 更改地區(Change Locale)：zh_TW.UTF-8 UTF-8 按下空白建、OK，選擇 zh_TW.UTF-8，按下OK\
8.進入 Localisation Options 更改時區(Change Timezone)，選擇 Asia，選擇 Taipei，按下OK\
9.進入 Localisation Options 更改wifi(Change Wi-fi Country)，選擇 TW Taiwan，按下OK\
10.進入 Interfacing Option 更改I2C為Enabled，按下OK\
11.重新啟動(sudo reboot)\
12.欲使用螢幕(HDMI)請修改config.txt的檔案，其中內容：\
uncomment to force a specific HDMI mode (this will force VGA)\
hdmi_group=2\
hdmi_mode=16\
\
取消下列程式碼：\
uncomment to force a HDMI mode rather than DVI. This can make audio work in\
DMT (computer monitor) modes\
hdmi_drive=2\
\
\
二、更新、新增套件\
1.sudo apt-get update\
2.sudo apt-get -y dist-upgrade & sudo apt-get upgrade(要按q繼續安裝) & sudo rpi-update\
3.sudo reboot\
4.sudo apt-get install -y i2c-tools\
5.sudo apt-get install python-smbus 在python上使用i2c\
6.進入 sudo apt-get install python-smbus\
7.進入sudo nano /boot/config.txt，取消 #device_tree_param=i2c_arm=on 的註解，若無則直接新增一行，並添加 dtparam=i2c1_baudrate=50000 更改i2c鮑率至 標準鮑率：100KHz 以下(1鮑即指每秒傳輸1個符號)。^x退出，y確定保存，enter以同一檔名保存\
7.進入 sudo nano /boot/cmdline.txt，至文件末尾添加一行 bcm2708.vc_i2c_override=1，^x退出，y確定保存，enter以同一檔名保存\
8.進入 sudo nano /etc/modules-load.d/raspberrypi.conf，至文件末尾添加 i2c-bcm2708 和 i2c-dev，^x退出，y確定保存，enter以同一檔名保存\
9.以 sudo i2cdetect -y 1 偵測 GPIO 上的裝置是否存在，如：\
pi@xxxxxxx:~ $ sudo i2cdetect -y 1\
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f\
00:          -- -- -- -- -- -- -- -- -- -- -- -- --\
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --\
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --\
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --\
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --\
50: -- -- -- -- -- -- -- -- -- -- 5a -- -- -- -- --\
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --\
70: -- -- -- -- -- -- 76 --\
\
10.安裝 pip：sudo apt-get install python-pip（或python3-pip）\
11.安裝 git-core： (1)sudo apt-get update (2)sudo apt-get upgrade (3)sudo apt-get install git-core\
\
PiCam：\
12.安裝 opencv：sudo apt-get install python-opencv\
13.啟用pi相機：sudo raspi-config，進入 Interfacing Options，啟用 P1/Camera，並且重啟。\
14.安裝 PeachPy  和  confu：(1)sudo pip install --upgrade git+https://github.com/Maratyszcza/PeachPy (2)sudo pip install --upgrade git+https://github.com/Maratyszcza/confu \
15.安裝忍者：(1) git clone https://github.com/ninja-build/ninja.git (2)cd ninja (3)git checkout release (4)./configure.py --bootstrap (5)export NINJA_PATH=$PWD (6)cd\
16.安裝修改後的 NNPACK：(1)git clone https://github.com/shizukachan/NNPACK (2)cd NNPACK (3)confu setup (4)python ./configure.py --backend auto (5)$NINJA_PATH/ninja(此步驟可能造成當機，請重作上個步驟的(5)，指定環境變數給NNPACK，請確認GPU可使用記憶體大小不大於64，大於64可能造成當機，若因為部分因素無法調整GUP使用大小，請使用Putty等CUI遠端登入介面，以減少記憶體資源占用。) (6)如果上述步驟成功，使用ls確認是否存在資料 lib (7)測試NNPACK是否正常工作：bin/convolution-inference-smoketest(此步驟如果有FAIL，請注意看錯誤報告，並重新安裝。) (8)將庫和頭文件複製到系統環境：(1)sudo cp -a lib/* /usr/lib/ (2)sudo cp include/nnpack.h /usr/include/ (3)sudo cp deps/pthreadpool/include/pthreadpool.h /usr/include/\
17.安裝darknet-nnpackcd (yolov3分支)：(1)cd (2)git clone -b yolov3 https://github.com/zxzhaixiang/darknet-nnpack (3)cd darknet-nnpack (4)git checkout yolov3 (4)make\
18.對於受限環境，我們選用較小的模型：yolov3-tiny。要使用此模型，請先下載權重：wget https://pjreddie.com/media/files/yolov3-tiny.weights \
然後使用tiny版本的配置文件和權重運行檢測器：./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights data/dog.jpg\
19.cd\
\
三、遠端\
1.下載teamviewer：wget http://download.teamviewer.com/download/linux/version_11x/teamviewer-host_armhf.deb \
2.sudo apt-get install -f\
3.安裝teamviewer：sudo dpkg -i teamviewer-host_armhf.deb\
4.有可能發生無法安裝teamviewer的情況，請先安裝libqt5webkit5：sudo apt-get install libqt5webkit5，有可能還是有問題，請修復安裝：sudo apt --fix-broken install\
\
四、開始執行\
1.進到github網站 https://github.com/OdinsHat/cjmcu-8128-sensor-breakout 此網站提供了CJMCU-8128的套件及範例程式。下載壓縮檔，解壓縮後利用FileZilla放入 /home/pi 目錄底下\
2.安裝Adafruit套件：(1)pip install Adafruit_CCS811 (2)pip install Adafruit_BME280\
3.進入範例程式目錄 cd prj/examples，執行.py檔案即可 ex:python cc811.py\
4.新建的資料請將Adafruit_BME280.py、Adafruit_CCS811.py、SDL_Pi_HDC1000.py，以及自己編寫的程式碼(.py)放在同一個目錄下\
