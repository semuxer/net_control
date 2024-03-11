import json


class ver():
    def __init__(self, verfname='version.json'):
        self.verfname = verfname
        with open(self.verfname, 'r', encoding="utf-8") as f:
            self.data = json.load(f)

    def getver(self):
        return f"{self.data.get('ver')}.{self.data.get('bild')}"

    def incver(self):
        self.data['ver'] += 1
        with open(self.verfname, 'w', encoding="utf-8") as f:
            json.dump(self.data, f)

    def incbuild(self):
        self.data['bild'] += 1
        with open(self.verfname, 'w', encoding="utf-8") as f:
            json.dump(self.data, f)


if __name__ == "__main__":
    version = ver()
    print(version.getver())
