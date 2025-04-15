# spx/cosmic.py
# SPX Protocol cosmic by Shaan (github.com/shaa2020)

from typing import Dict

class CosmicTrace:
    def _init_(self):
        self.events = []

    def span(self, name: str):
        class Span:
            def _init_(self, name):
                self.name = name
            def _enter_(self):
                print(f"🌌 {self.name} started")
                self.events.append({"type": "span_start", "name": self.name})
            def _exit_(self, *args):
                print(f"🌌 {self.name} ended")
                self.events.append({"type": "span_end", "name": self.name})
        return Span(name)

    def metric(self, name: str, value: float):
        print(f"⭐ {name}: {value}")
        self.events.append({"type": "metric", "name": name, "value": value})

    def get_events(self):
        return self.events