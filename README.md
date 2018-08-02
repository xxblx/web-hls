
# web-hls 

Web-hls is a very simple prototype of a tool for streaming video from ip cameras (rtsp) to web (hls). Originally web-hls was designed for personal usage at home's local network. This tool is not suitable for using in the production. 

Web-hls is licensed under zlib/libpng. See LICENSE for details.

# Installation

Create user 
```
# useradd hlshoster -m -s /sbin/nologin
```

Edit `ffmpeg-hls@.service` and copy it to `/etc/systemd/system`, start and enable unit

```
# systemctl start ffmpeg-hls@rtsp://ip:port  # replace rtsp://ip:port with your input
# systemctl enable ffmpeg-hls@rtsp://ip:port
```

Create virtual environment and install packages under `hlshoster` user
```
$ python3 -m venv VENV  # make virtual environment
$ VENV/bin/pip install tornado bcrypt  # install packages
```

Edit `web-hls.service` and copy it `/etc/systemd/system`, start and enable unit 
```
# systemctl start web-hls.service
# systemctl enable web-hls.service
```

