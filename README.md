# FreeCAD OpenAGI Agent Scripts

This project demonstrates using OpenAGI agents to automate FreeCAD PartDesign tasks with various levels of human guidance and interaction.

---

## ⭐ **RECOMMENDED: Dynamic Guidance System**

### `dynamic_guided_hello.py`
**The most powerful approach - allows real-time guidance injection while the agent runs.**

This script runs the agent with a dynamic feedback system that allows you (or another AI) to inject guidance mid-execution when the agent gets stuck or makes mistakes.

**How it works:**
- Agent runs continuously, checking for guidance at each step
- When issues are detected, write guidance to `/tmp/freecad_agent_guidance.json`
- Agent automatically picks up and applies the new todos
- No restart needed - guidance is injected seamlessly

**Usage:**
```bash
python dynamic_guided_hello.py
```

**To provide guidance while running:**
```bash
cat > /tmp/freecad_agent_guidance.json << 'EOF'
{
  "todos": [
    "New instruction 1",
    "New instruction 2"
  ],
  "message": "Helpful context about what went wrong"
}
EOF
```

**Helper script:**
```bash
python send_guidance.py "First todo" "Second todo" "Third todo"
```

**Key Features:**
- ✅ Real-time monitoring and guidance injection
- ✅ No restart required when agent gets stuck
- ✅ Exports detailed execution log to markdown
- ✅ Works like human-in-the-loop but can be automated

---

## Other Agent Scripts

### `hello.py`
**The original base script with improved prompts.**

A straightforward agent execution with enhanced, detailed prompts for each FreeCAD PartDesign step. No interactive features - just runs start to finish.

**Usage:**
```bash
python hello.py
```

**Best for:**
- Simple, unattended execution
- Testing prompt improvements
- Baseline performance comparison

---

### `auto_guided_hello.py`
**Automated monitoring with contextual guidance.**

Runs the agent with an observer that automatically provides guidance based on event types. Includes automatic logging and markdown export.

**Usage:**
```bash
python auto_guided_hello.py
```

**Features:**
- Automatic guidance based on event patterns
- 2-second delay between steps for observation
- Exports execution log to `freecad_execution_log.md`
- Error detection and recovery suggestions

---

### `interactive_hello.py`
**Human-interactive mode with manual control.**

Pauses after each step and prompts for human input. Allows manual todo injection and execution control.

**Usage:**
```bash
python interactive_hello.py
```

**Commands:**
- `continue` - Proceed to next step
- `stop` - Stop execution
- `add [instruction]` - Add a new todo
- `help` - Show available commands

**Best for:**
- Debugging agent behavior
- Learning how the agent works
- Step-by-step validation

---

### `monitored_hello.py`
**Non-interactive observation mode.**

Similar to auto_guided but focuses on monitoring rather than guidance. Logs all steps without pausing.

**Usage:**
```bash
python monitored_hello.py
```

**Features:**
- Continuous logging
- 1-second delay between steps
- Can be interrupted with Ctrl+C
- Good for passive observation

---

### `send_guidance.py`
**Helper utility for dynamic guidance.**

Simplifies sending guidance to a running `dynamic_guided_hello.py` instance.

**Usage:**
```bash
python send_guidance.py "Todo 1" "Todo 2" "Todo 3"
```

---

## FreeCAD Task Description

All scripts automate the following PartDesign workflow:

1. ✅ Verify PartDesign workbench is active
2. ✅ Create a new Body
3. ✅ Create a new Sketch on XY plane
4. ✅ Draw a 20mm × 20mm rectangle centered on origin
5. ✅ Draw a 10mm diameter circle at center
6. ✅ Apply dimensional constraints
7. ✅ Verify sketch is fully constrained
8. ✅ Close the sketch
9. ✅ Pad (extrude) the sketch by 20mm

**Result:** A 20mm cube with a 10mm cylindrical hole through the center.

---

## Key Learnings

### What Works Well
- ✅ **Dynamic guidance system** - Can course-correct in real-time
- ✅ **Detailed prompts** - Specific menu paths and button descriptions help
- ✅ **Breaking down complex tasks** - Separate todos for find tool vs. use tool
- ✅ **Menu-based navigation** - More reliable than toolbar icon hunting

### Common Challenges
- ⚠️ **Toolbar icon identification** - Agents struggle with similar-looking icons
- ⚠️ **Workbench confusion** - Easy to end up in Part vs. PartDesign
- ⚠️ **Constraint application** - Finding the right constraint buttons is difficult
- ⚠️ **Dialog handling** - Accidentally opening wrong dialogs requires recovery

### Solutions Implemented
1. **Explicit menu paths** - "Sketch menu > Sketcher geometries > Create rectangle"
2. **Visual descriptions** - "looks like a pencil/sheet icon"
3. **Alternative approaches** - Provide both toolbar and menu options
4. **Dynamic feedback** - Inject corrections when agent goes off track

---

## Model Information

All scripts use the `lux-thinker-1` model from the OpenAGI platform.

**Model characteristics:**
- Max steps capped at 120 per subtask
- Good at reasoning about UI elements
- Benefits from detailed, specific instructions
- Can recover from mistakes with guidance

---

## Requirements

```bash
pip install oagi
```

**Environment:**
- Python 3.12+
- FreeCAD installed and visible
- OpenAGI API access

---

## Execution Logs

When using `auto_guided_hello.py` or `dynamic_guided_hello.py`, execution logs are exported to:
- `freecad_execution_log.md` - Full execution trace with screenshots
- `images/` - Screenshot images from execution

---

## Future Improvements

1. **Workbench enforcement** - Add checks to ensure PartDesign stays active
2. **Visual verification** - Verify sketch constraints visually before proceeding
3. **Error recovery patterns** - Build library of common mistakes and fixes
4. **Multi-part assemblies** - Extend to create complex parts

---

## Contributing

When improving prompts, focus on:
- Specific UI element locations (menu paths, coordinates)
- Visual descriptions of buttons and icons
- Alternative approaches when primary path fails
- Clear success criteria for each step

---

**Happy automating! 🤖**
