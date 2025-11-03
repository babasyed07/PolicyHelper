#!/usr/bin/env python3
import sys
from history_manager import HistoryManager

def main():
    history = HistoryManager()
    entries = history.get_history()
    
    if not entries:
        print("No policy history found.")
        return
    
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        index = int(sys.argv[1])
        entry = history.get_policy(index)
        if entry:
            print(f"Policy #{index}")
            print(f"Timestamp: {entry['timestamp']}")
            print(f"Requirement: {entry['requirement']}")
            print(f"\nPolicy:\n{entry['policy']}")
            print(f"\nRationale:")
            for rationale in entry['rationale']:
                print(rationale)
        else:
            print(f"Policy #{index} not found.")
    else:
        print("Policy History:")
        for i, entry in enumerate(entries):
            print(f"#{i}: {entry['requirement'][:50]}... ({entry['timestamp'][:10]})")

if __name__ == "__main__":
    main()