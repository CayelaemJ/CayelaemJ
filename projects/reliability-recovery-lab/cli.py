"""Run the fictional retry and recovery timeline in a terminal."""
import json
from reliability import demonstration

if __name__ == "__main__":
    print(json.dumps(demonstration(), indent=2))
