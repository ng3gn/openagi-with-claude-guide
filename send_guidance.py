#!/usr/bin/env python3
"""Helper script to send dynamic guidance to the running agent."""

import json
import sys

GUIDANCE_FILE = "/tmp/freecad_agent_guidance.json"

def send_guidance(todos=None, message=None):
    """Send guidance to the running agent.

    Args:
        todos: List of todo strings to add
        message: Optional message to display
    """
    guidance = {}

    if todos:
        guidance['todos'] = todos if isinstance(todos, list) else [todos]

    if message:
        guidance['message'] = message

    with open(GUIDANCE_FILE, 'w') as f:
        json.dump(guidance, f, indent=2)

    print(f"✓ Guidance sent: {guidance}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python send_guidance.py \"todo text\"")
        print("  python send_guidance.py \"todo 1\" \"todo 2\" \"todo 3\"")
        sys.exit(1)

    todos = sys.argv[1:]
    send_guidance(todos=todos, message=f"Added {len(todos)} new todo(s)")
