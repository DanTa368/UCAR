import json


class DarknetResult:
    def __init__(self, data):
        js = json.loads(data)
        self.label = js["label"]
        self.x = js["x"]
        self.y = js["y"]
        self.w = js["w"]
        self.h = js["h"]
        self.confidence = js["confidence"]

    def __str__(self) -> str:
        return json.dumps(
            {"label": self.label, "x": self.x, "y": self.y, "w": self.w, "h": self.h, "confidence": self.confidence})
