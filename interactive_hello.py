import asyncio
from oagi import AsyncScreenshotMaker, AsyncPyautoguiActionHandler, TaskerAgent, AsyncAgentObserver

class InteractiveObserver(AsyncAgentObserver):
    """Observer that provides feedback and allows for dynamic guidance."""

    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.step_count = 0

    async def on_event(self, event):
        """Called when an event occurs during agent execution."""
        # Store the event
        await super().on_event(event)

        self.step_count += 1

        print(f"\n{'='*60}")
        print(f"STEP {self.step_count}")
        print(f"{'='*60}")

        # Display current todo if available
        if hasattr(self.agent, 'current_todo_index'):
            print(f"Current todo index: {self.agent.current_todo_index}")

        # Display event information
        print(f"Event type: {type(event).__name__}")

        # Show relevant event details
        if hasattr(event, '__dict__'):
            for key, value in event.__dict__.items():
                if key in ['screenshot', 'image', 'raw_image']:
                    print(f"{key}: [Image data - {type(value).__name__}]")
                elif isinstance(value, str) and len(value) > 200:
                    print(f"{key}: {value[:200]}...")
                elif not key.startswith('_'):
                    print(f"{key}: {value}")

        # Interactive prompt
        print(f"\n{'='*60}")
        user_input = input("Enter command (continue/stop/add [instruction]/help): ").strip().lower()

        if user_input == 'stop':
            print("Stopping execution...")
            raise KeyboardInterrupt("User requested stop")
        elif user_input.startswith('add '):
            instruction = user_input[4:].strip()
            if instruction:
                self.agent.append_todo(instruction)
                print(f"Added new todo: {instruction}")
        elif user_input == 'help':
            print("\nAvailable commands:")
            print("  continue - Continue to next step")
            print("  stop - Stop execution")
            print("  add [instruction] - Add a new todo to the list")
            print("  help - Show this help message")

async def main():
    agent = TaskerAgent(model="lux-thinker-1")

    # Set up the observer
    observer = InteractiveObserver(agent)
    agent.step_observer = observer

    agent.set_task(
        task="Use FreeCAD to make a part with PartDesign workbench",
        todos=[
            "Ensure you are in the PartDesign workbench. Look at the workbench dropdown at the top toolbar to verify.",
            "Create a new Body if one doesn't exist: Click 'Create Body' button in the PartDesign toolbar or menu.",
            "Create a new sketch: Click the 'Create Sketch' button (looks like a pencil/sheet icon) in the PartDesign toolbar.",
            "Select the XY plane: In the dialog that appears, click on 'XY_Plane' option and click OK button.",
            "Draw a rectangle: Use the rectangle tool (polyline or rectangle icon in sketch toolbar) to draw a square roughly centered on the origin.",
            "Set rectangle dimensions: Select the rectangle, then use the constraint tools to set horizontal and vertical distances to 20mm. Make sure all 4 sides are constrained.",
            "Center the rectangle: Add symmetric or coincident constraints to center the rectangle on the origin (0,0). The rectangle corners should be equidistant from the origin.",
            "Draw a circle: Use the circle tool to draw a circle at the center (origin) of the rectangle.",
            "Constrain circle diameter: Select the circle, then use the radius/diameter constraint to set it to 10mm diameter (5mm radius).",
            "Verify the sketch is fully constrained: The sketch should turn green when fully constrained. All elements should have no degrees of freedom remaining.",
            "Close the sketch: Click the 'Close' button in the sketch toolbar, or press Escape key to exit sketch mode.",
            "Apply Pad feature: With the sketch selected in the tree view, click the 'Pad' button (first icon in PartDesign toolbar showing an extruded shape). In the Pad dialog, set the length to 20mm and click OK.",
        ]
    )

    print("Starting interactive session with OpenAGI agent...")
    print("You will be prompted after each step to continue, stop, or add new instructions.\n")

    result = await agent.execute(
        instruction="Use FreeCAD to make a part with PartDesign workbench",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    print(f"\n{'='*60}")
    print(f"Execution completed: {result}")
    print(f"Total steps: {observer.step_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
