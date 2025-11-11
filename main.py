import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dali import Dali

if __name__ == "__main__":
    try:
        dali = Dali()
        dali.start()
    except Exception as e:
        print(f"❌ Failed to start Dali: {e}")
        print("Make sure all dependencies are installed.")
