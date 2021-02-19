# FuckCoolDownBot

This is my fucking bot script for fucking responding to u/CoolDownBot's fucking posts.

### Instructions

1. Go to https://old.reddit.com/prefs/apps/
2. Create a new app
3. Give it a name, check "Script" and set the URLs to "http://localhost". Click "Create app".
4. Take note of the following values:

```
client_id -> the string right under "Personal Use Script"
client_secret -> labeled as "secret"
```

5. Clone this repo to `~/FuckCoolDownBot`

6. Make a `~/.configs/praw.ini` file with the following contents, filling in your own values

```
[FuckCoolDownBot2]
client_id=XXXXXXXXX
client_secret=XXXXXXXXXXXXXXXXXXXX
password=XXXXXXXXXXXXXXXXXX
username=XXXXXXXXXXXXXXXX
```

7. Install Python dependencies

```
$ python3 -m pip install -r requirements.txt
```
8. Run bot with `python3 bot.py`

### Bonus

Start automatically as a service - figure it out :)

1. Edit `fuckcooldownbot.service` and replace `pi` with your username
2. Copy `fuckcooldownbot.service` to `/etc/systemd/system/fuckcooldownbot.service`. `sudo cp fuckcooldownbot.service /etc/systemd/system/fuckcooldownbot.service`
3. Reload systemd daemon `sudo systemctl daemon-reload`
4. Enable and start bot

```
sudo systemctl enable fuckcooldownbot.service
sudo systemctl start fuckcooldownbot.service
```

5. ...
6. Profit
