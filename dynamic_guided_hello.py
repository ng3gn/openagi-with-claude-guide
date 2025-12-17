import asyncio
import os
import json
from pathlib import Path
from oagi import AsyncScreenshotMaker, AsyncPyautoguiActionHandler, TaskerAgent, AsyncAgentObserver

# Shared file for dynamic guidance
GUIDANCE_FILE = "/tmp/freecad_agent_guidance.json"

class DynamicGuidanceObserver(AsyncAgentObserver):
    """Observer that checks for and applies dynamic guidance during execution."""

    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.step_count = 0
        self.paused = False
        self.guidance_file = Path(GUIDANCE_FILE)

        # Clear any existing guidance file
        if self.guidance_file.exists():
            self.guidance_file.unlink()

    async def on_event(self, event):
        """Called when an event occurs during agent execution."""
        await super().on_event(event)

        self.step_count += 1

        print(f"\n{'='*60}")
        print(f"STEP {self.step_count}")
        print(f"{'='*60}")

        # Display current todo
        if hasattr(self.agent, 'current_todo_index'):
            current_idx = self.agent.current_todo_index
            try:
                memory = self.agent.get_memory()
                if 'todos' in memory and current_idx < len(memory['todos']):
                    current_todo = memory['todos'][current_idx]
                    print(f"Current todo [{current_idx+1}/{len(memory['todos'])}]: {current_todo}")
            except:
                pass

        # Display event information
        event_type = type(event).__name__
        print(f"Event type: {event_type}")

        # Check for dynamic guidance
        await self._check_and_apply_guidance()

        # Display event details
        if hasattr(event, '__dict__'):
            for key, value in event.__dict__.items():
                if key in ['screenshot', 'image', 'raw_image']:
                    print(f"{key}: [Image data - {type(value).__name__}]")
                elif isinstance(value, str) and len(value) > 200:
                    print(f"{key}: {value[:200]}...")
                elif not key.startswith('_'):
                    print(f"{key}: {value}")

        print(f"{'='*60}\n")

    async def _check_and_apply_guidance(self):
        """Check for guidance file and apply any new todos."""
        if self.guidance_file.exists():
            try:
                with open(self.guidance_file, 'r') as f:
                    guidance = json.load(f)

                print(f"\n{'*'*60}")
                print(f"📝 DYNAMIC GUIDANCE RECEIVED")
                print(f"{'*'*60}")

                # Apply new todos
                if 'todos' in guidance:
                    for todo in guidance['todos']:
                        print(f"  Adding todo: {todo}")
                        self.agent.append_todo(todo)

                # Display message if provided
                if 'message' in guidance:
                    print(f"  Message: {guidance['message']}")

                print(f"{'*'*60}\n")

                # Remove the guidance file after reading
                self.guidance_file.unlink()

                # Small delay to let user see the message
                await asyncio.sleep(1)

            except Exception as e:
                print(f"Error reading guidance file: {e}")

async def main():
    agent = TaskerAgent(model="lux-thinker-1")

    # Set up the observer
    observer = DynamicGuidanceObserver(agent)
    agent.step_observer = observer

    # Configure agent parameters
    agent.step_delay = 2.0  # 2 second delay between steps
    agent.max_steps = 150

    agent.set_task(
        task="Create a 20mm x 30mm x 40mm rectangular prism with one corner at the origin using PartDesign",
        todos=[
            "Switch to PartDesign workbench: Click the workbench dropdown (shows 'Part' or similar), then click 'PartDesign' from the list.",
            "Create Body: Click 'Create Body' in PartDesign toolbar. When 'Select Attachment' dialog appears, simply click OK to accept defaults.",
            "Start new sketch: In Tasks panel on right, click 'New Sketch'. When plane selection appears, click 'XY_Plane' or 'XY-plane', then click OK.",
            "Activate rectangle tool: Click Sketch menu, hover over 'Sketcher geometries', then click 'Create rectangle'. The rectangle tool is now active.",
            "Draw rectangle from origin: Click at origin point (0,0), then click at coordinates approximately (20, 30). Rectangle is now drawn.",
            "Lock corner to origin: Click the bottom-left corner point of rectangle. Click Sketch menu > 'Constrain coincident'. This locks corner to origin.",
            "Set width to 20mm: Click the BOTTOM EDGE (horizontal line) of rectangle. Click Sketch menu > 'Constrain horizontal distance'. Type 20, click OK.",
            "Set height to 30mm: Click the LEFT EDGE (vertical line) of rectangle. Click Sketch menu > 'Constrain vertical distance'. Type 30, click OK.",
            "Close sketch: Click 'Close' button in the Tasks panel on the right side. This exits sketch mode and returns to PartDesign.",
            "Extrude to 40mm: Click 'Pad' button in PartDesign toolbar (shows box with up arrow). In dialog, change Length to 40, then click OK. Done!",
        ]
    )

    print("="*60)
    print("DYNAMIC GUIDANCE SYSTEM ACTIVE")
    print("="*60)
    print(f"To provide guidance, write to: {GUIDANCE_FILE}")
    print("Format: {\"todos\": [\"todo 1\", \"todo 2\"], \"message\": \"optional message\"}")
    print("="*60)
    print("\nStarting agent execution...\n")

    try:
        result = await agent.execute(
            instruction="Use FreeCAD to make a part with PartDesign workbench",
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

        print(f"\n{'='*60}")
        print(f"EXECUTION COMPLETE")
        print(f"{'='*60}")
        print(f"Result: {result}")
        print(f"Total steps: {observer.step_count}")
        print(f"{'='*60}")

        # Export the full event log
        print("\nExporting detailed event log...")
        observer.export('markdown', 'freecad_execution_log.md', 'images')
        print("Log exported to: freecad_execution_log.md")

    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user.")
        print(f"Completed {observer.step_count} steps before interruption.")
    except Exception as e:
        print(f"\n\nExecution error: {e}")
        print(f"Completed {observer.step_count} steps before error.")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
