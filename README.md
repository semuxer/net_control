# net_control

This program is designed to test communications with selected hosts at specified intervals.

Before use, make changes to the configuration file <config.json>

```python
{
    "8.8.8.8": { # host address
        "name": "ДНС Google", # Alias.
        "media": "error.mp3", # Sound file to be played if there is no connection.
        "timeout": 50, # Time between polls is seconds.
        "skiperrors": 1 # The number of mistakes you can miss. Use to filter out fake disconnections.
    },
    "google.com": {
        "name": "Google",
        "media": "error.mp3",
        "timeout": 2,
        "skiperrors": 2
    }
}
```


Author: Sergey Movchan, 2024
