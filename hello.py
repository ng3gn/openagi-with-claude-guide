import asyncio

# Captures the screenshot from your local computer
from oagi import AsyncScreenshotMaker

# Controls your local keyboard and mouse based on the model predicted actions
from oagi import AsyncPyautoguiActionHandler
from oagi import TaskerAgent

async def main():
    agent = TaskerAgent(model="lux-thinker-1")

    agent.set_task(
        task="Create a 20mm cube with 10mm center hole using PartDesign",
        todos=[
            "Switch to PartDesign workbench: Click workbench dropdown, select 'PartDesign'.",
            "Create Body: Click 'Create Body' button. When dialog appears, click OK.",
            "Start sketch: In Tasks panel, click 'New Sketch'. Select 'XY_Plane', click OK.",
            "Activate rectangle tool: Sketch menu > 'Sketcher geometries' > 'Create rectangle'.",
            "Draw 20mm square centered on origin: Click at (-10, -10), then click at (10, 10).",
            "Set horizontal size: Click TOP EDGE. Sketch menu > 'Constrain horizontal distance'. Enter 20, click OK.",
            "Set vertical size: Click LEFT EDGE. Sketch menu > 'Constrain vertical distance'. Enter 20, click OK.",
            "Center on origin: Click opposite corners (top-right and bottom-left). Sketch menu > 'Constrain symmetric'. Click origin point.",
            "Draw center circle: Sketch menu > 'Sketcher geometries' > 'Create circle'. Click origin (0,0), drag out and click to set size.",
            "Set circle diameter: Click the circle. Sketch menu > 'Constrain diameter'. Enter 10, click OK.",
            "Close sketch: Click 'Close' in Tasks panel.",
            "Extrude 20mm: Click 'Pad' button. Set Length to 20, click OK. Done!",
        ]
    )

    await agent.execute(
        instruction="Use FreeCAD to make a part with PartDesign workbench",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

asyncio.run(main())
