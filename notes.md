#### server at reboot
- `sudo apt update`
- `sudo apt install nginx`
- `sudo pip install flask uwsgi`
- [?] Confirm flask app `__name__ == "__main__"` is uncommented 
- confirm **uwsgi.ini** in matrix_spi dir
- Add www-data to gpio group - `sudo usermod -a -G gpio www-data`
- `sudo rm /etc/nginx/sites-enabled/default`
- `sudo nano /etc/nginx/sites-available/matrix_spi_proxy`
  
```
server {
listen 80;
server_name localhost;

location / { try_files $uri @app; }
location @app {
include uwsgi_params;
uwsgi_pass unix:/tmp/matrix_spi.sock;
}
}
```

- `sudo ln -s /etc/nginx/sites-available/flasktest_proxy /etc/nginx/sites-enabled`
- `sudo systemctl restart nginx`
- Test - 502 bad gateway
- `sudo nano /etc/systemd/system/uwsgi.service`
- Confirm location of /usr/local/bin/uwsgi

```
[Unit]
Description=uWSGI Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/pi/matrix_spi/
ExecStart=/usr/local/bin/uwsgi --ini /home/pi/matrix_spi/uwsgi.ini

[Install]
WantedBy=multi-user.target
```

- `sudo systemctl daemon-reload`
- `sudo systemctl start uwsgi.service`
- Check status - `sudo systemctl status uwsgi.service`
- Run at reboot - `sudo systemctl enable uwsgi.service`
- Add auto reload `touch-reload = /home/pi/matrix_spi/app.py`