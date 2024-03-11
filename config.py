import json


class conf():
    def __init__(self, confname):

        try:
            with open(confname, 'r', encoding="utf-8") as f:
                self.data = json.load(f)

        except:
            self.data = {
                "8.8.8.8": {
                    "name": "ДНС Google",
                    "media": "error.mp3",
                    "timeout": 5,
                    "skiperrors": 1
                },
                "google.com": {
                    "name": "Google",
                    "media": "error.mp3"
                }
            }

            # Запись в файл JSON
            with open(confname, 'w', encoding="utf-8") as f:
                json.dump(self.data, f)

        # defaults datas
        for host, d in self.data.items():
            self.data[host]["name"] = self.data[host].get('name', "")
            self.data[host]["media"] = self.data[host].get(
                'media', "error.mp3")
            self.data[host]["timeout"] = self.data[host].get('timeout', 5)
            self.data[host]["timecount"] = 0
            self.data[host]["skiperrors"] = self.data[host].get(
                'skiperrors', 1)
            self.data[host]["skipecount"] = self.data[host].get('skiperrors')
            self.data[host]["status"] = 3


if __name__ == "__main__":
    config = conf('config.json')
    print(config.data)
