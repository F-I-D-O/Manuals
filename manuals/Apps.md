
# Slack

## Notifications
[Official Manual](https://slack.com/help/articles/360025446073-Guide-to-Slack-notifications)

There are two kinds of notifications in slack:

- Pop-up notifications, including the beginning of the text message
- Icon notifications: on the tray icon on PC and on the app icon on cell phone

### Icon notifications
Threre are two types of icon notifications:

- **red**: for direct message, mention,, thread replies, or a keyword match. Basically, anything that trigers a popup should raise the red icon
- **blue**: any unread activity, with exception of the muted chanels


### Muting channels
[Official Manual](https://slack.com/intl/en-gb/help/articles/204411433-Mute-channels-and-direct-messages)

For each channel, there are three settings. Their effect is summarized in the following table:

| Setting | pop-ups - mentions | pop-ups - all | icon notif. - mentions | icon notif. - all |
| --- | --- | --- | --- | --- |
| `All new posts` | yes | yes | yes | yes |
| `Just mentions` | yes | no | yes | yes |
| `Mute and hide` | no | no | yes | no |



# Syncthing
[Official documentation](https://docs.syncthing.net/)

## Autostart
[Official documentation](https://docs.syncthing.net/users/autostart.html)

By default, we need to start the Syncthing manually. However, several ways of automating the startup are described in the documentation.

# Toggle

## Troubleshooting


### Synchronization fails
To resolved failed sync, we can use the sync button (or down slide on Android). If that does not work. Follow these steps:

1. check if there are any entries in the app that are not online (in the web app).
1. If there are any, export them to csv
1. Import the entries online
1. Log out, then log back in


