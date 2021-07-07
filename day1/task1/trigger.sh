#!/bin/bash
sudo cat /var/log/dmesg > /home/log.txt
sudo mount /dev/sdf1 /media/usb
sudo cat /var/log/boot.log > /media/usb/logs/boot.log
sudo cat /var/log/dmesg > /media/usb/logs/dmesg.log
sudo umount /media/usb
