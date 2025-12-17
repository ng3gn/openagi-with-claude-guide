import asyncio

# Captures the screenshot from your local computer
from oagi import AsyncScreenshotMaker

# Controls your local keyboard and mouse based on the model predicted actions
from oagi import AsyncPyautoguiActionHandler
from oagi import TaskerAgent

async def main():
    agent = TaskerAgent(model="lux-thinker-1")

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

    await agent.execute(
        instruction="Use FreeCAD to make a part with PartDesign workbench",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

asyncio.run(main())
