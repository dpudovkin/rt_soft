# Launch Firefox GUI application

## Instruction

```sh
sudo apt get install xorg xauth openbox
sudo docker build -t firefox_browser
sudo docker run -e DISPLAY -v $HOME/.Xauthotiry:/home/username/.Xauthority --net=host firefox_browser
```



