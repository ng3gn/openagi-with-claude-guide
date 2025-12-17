import asyncio
from oagi import AsyncScreenshotMaker, AsyncPyautoguiActionHandler, TaskerAgent, AsyncAgentObserver

class AutoGuidedObserver(AsyncAgentObserver):
    """Observer that automatically provides guidance based on events."""

    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.step_count = 0
        self.error_count = 0
        self.guidance_log = []

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

        # Provide guidance based on event type
        guidance = self._provide_guidance(event, event_type)
        if guidance:
            print(f"\n[GUIDANCE] {guidance}")
            self.guidance_log.append({
                'step': self.step_count,
                'event_type': event_type,
                'guidance': guidance
            })

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

    def _provide_guidance(self, event, event_type):
        """Analyze event and provide contextual guidance."""

        # Check for common issues
        if event_type == 'ErrorEvent' or (hasattr(event, 'message') and 'error' in str(event.message).lower()):
            self.error_count += 1
            return f"Error detected (#{self.error_count}). Agent should retry or try an alternative approach."

        # Provide guidance for specific event types
        if event_type == 'SplitEvent':
            return "Starting new todo task."

        if event_type == 'ActionEvent':
            if hasattr(event, 'action_type'):
                action_type = event.action_type
                if action_type == 'click':
                    return "Click action performed. Verify the correct element was clicked."
                elif action_type == 'type':
                    return "Text input action. Ensure the correct field is focused."

        if event_type == 'ThinkEvent':
            return "Agent is analyzing the current state."

        return None

async def main():
    agent = TaskerAgent(model="lux-thinker-1")

    # Set up the observer
    observer = AutoGuidedObserver(agent)
    agent.step_observer = observer

    # Configure agent parameters
    agent.step_delay = 2.0  # 2 second delay between steps for observation
    agent.max_steps = 150  # Reasonable limit

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

    print("Starting auto-guided session with OpenAGI agent...")
    print("The agent will execute with automated guidance and monitoring.\n")

    try:
        result = await agent.execute(
            instruction="Use FreeCAD to make a part with PartDesign workbench",
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

        print(f"\n{'='*60}")
        print(f"EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Execution completed: {result}")
        print(f"Total steps: {observer.step_count}")
        print(f"Errors encountered: {observer.error_count}")
        print(f"Guidance provided: {len(observer.guidance_log)} times")
        print(f"{'='*60}")

        # Export the full event log
        print("\nExporting detailed event log to markdown...")
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
