from datetime import datetime
import json


class Timer:
    def __init__(self):
        self.started_at = None
        self.stopped_at = None

    def start(self, started_at=datetime.now()):
        self.started_at = started_at
        return self

    def stop(self, stopped_at=datetime.now()):
        self.stopped_at = stopped_at
        return self

    def __str__(self):
        current_time = datetime.now()
        delta = (self.stopped_at - self.started_at) if (
            isinstance(self.started_at, datetime) and isinstance(self.stopped_at, datetime)
        ) else (current_time - self.started_at)
        return json.dumps({
            'current_time': current_time.isoformat(),
            'started_at': self.started_at.isoformat() if isinstance(self.started_at, datetime) else None,
            'stopped_at': self.stopped_at.isoformat() if isinstance(self.stopped_at, datetime) else None,
            'total_seconds': delta.total_seconds(),
        })


if __name__ == '__main__':
    t = Timer()
    print(t.start())
    print(t)
    print(t.stop())
