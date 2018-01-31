```
First step: Update and upgrade the system packages.
All commands listed below shall be executed on the PI. 

$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo cp /usr/share/zoneinfo/Hongkong /etc/localtime
```
```
Second step: use apt to install required packages. 
All commands listed below shall be executed on the PI. 

$ sudo apt-get install openssh-server
$ sudo apt-get install python-requests
$ sudo apt-get install python-numpy
$ sudo apt-get install python-opencv
$ sudo apt-get install libimlib2-dev
$ wget --progress=bar 'https://www.unix-ag.uni-kl.de/~auerswal/ssocr/ssocr-2.16.4.tar.bz2'
$ tar -xjvf 'ssocr-2.16.4.tar.bz2'
$ cd ssocr-2.16.4
$ make
$ sudo make install
$ cd ..
$ rm -r ssocr-2.16.4/
$ rm ssocr-2.16.4.tar.bz2
```
```
第三步：scp上傳上三個文件和一個文件夾並創建images文件夾

On MAC or laptop: 
$ scp conf.json ustone@[ip]:~/
$ scp main.py ustone@[ip]:~/
$ scp send_email.py ustone@[ip]:~/
$ scp -r debug ustone@[ip]:~/debug

--在树莓派上：
$ sudo mkdir images
```
```
第五步：修改id？

$ sudo nano conf.json
```
```
第六步：創建ustone.service並啟用

$ sudo nano /lib/systemd/system/ustone.service

--加入以下并保存:

[Unit]
Description=UST.one Service
After=multi-user.target
[Service]
Type=idle
ExecStart=/usr/bin/python /home/ustone/main.py > /home/ustone/ustone.log 2>&1
[Install]
WantedBy=multi-user.target

--加入到此為止--

$ sudo chmod 644 /lib/systemd/system/ustone.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable ustone.service
$ sudo reboot
```
```
第七步：創建定時任務：ustone.service半小時重啟動

$ sudo crontab -e

--在文件最後加入以下并保存:

0,30 * * * * /bin/systemctl restart ustone.service

--加入到此為止--
```

