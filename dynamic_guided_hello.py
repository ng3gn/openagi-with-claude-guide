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
        task="Use FreeCAD to make a part with PartDesign workbench",
        todos=[
            "Ensure you are in the PartDesign workbench. Look at the workbench dropdown at the top toolbar to verify.",
            "Create a new Body if one doesn't exist: Click 'Create Body' button in the PartDesign toolbar or menu.",
            "Create a new sketch: Click the 'Create Sketch' button (looks like a pencil/sheet icon) in the PartDesign toolbar.",
            "Select the XY plane: In the dialog that appears, click on 'XY_Plane' option and click OK button.",
            "Find the rectangle tool: Look in the Sketch toolbar (usually appears when sketch mode is active). The rectangle tool may be under 'Sketch' menu > 'Sketcher geometries' > 'Create rectangle' OR as a rectangle icon in the sketch toolbar. Try clicking the Sketch menu first.",
            "Draw a rectangle: Click and drag from approximately (-10, -10) to (10, 10) to create a 20mm square centered roughly on the origin. Click once to start the rectangle, move the mouse, and click again to finish.",
            "Apply horizontal distance constraint: Click on the top edge of the rectangle to select it. Then click the 'Constrain horizontal distance' button (or Sketch menu > Constrain horizontal distance). Enter 20 in the dialog and click OK.",
            "Apply vertical distance constraint: Click on the left or right edge of the rectangle. Then click 'Constrain vertical distance'. Enter 20 and click OK.",
            "Center the rectangle on origin: Select opposite corners of the rectangle and add a symmetric constraint relative to the origin point (0,0). Use Sketch menu > 'Constrain symmetric' or the symmetric constraint button.",
            "Draw a circle at center: Click the circle tool from the sketch toolbar. Click once at the origin (0,0) to place the center, then click again to set the radius.",
            "Constrain circle diameter: Click on the circle to select it. Then click 'Constrain diameter' or 'Constrain radius' button. Enter 10 for diameter (or 5 for radius) and click OK.",
            "Verify sketch is fully constrained: Check that all sketch elements turn green. If any elements are white or blue, they need additional constraints. The sketch should show '0' degrees of freedom.",
            "Close the sketch: Look for a 'Close' button in the task panel on the right, or in the Sketch menu select 'Close sketch', or press Escape key.",
            "Apply Pad feature: Click the 'Pad' button in the PartDesign toolbar (looks like an extruded rectangle). In the Pad dialog, set Length to 20mm and click OK.",
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
