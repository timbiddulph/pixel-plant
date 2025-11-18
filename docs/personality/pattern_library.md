# Pixel Plant Pattern Library

## Overview

This document visualizes all available 8x8 pixel art patterns for the Pixel Plant LED matrix display. These patterns enable the Pixel Plant to express emotions and communicate messages through visual design.

## Pattern Legend

```
█ = Primary color (main features, outlines)
▓ = Secondary color (details, pupils, highlights)
░ = Accent color (special features, sparkles)
  = Background (off/black)
```

## Emotional Expressions

### Happy Face
**Use Case**: General contentment, normal operation, positive feedback
**Default Color**: Green (caring, healthy)

```

  █  █
  ▓  ▓

 █    █
  █  █
   ██

```

### Very Happy Face
**Use Case**: Celebration, user achieved goal, successful habit
**Default Color**: Yellow/Multi-color (joyful, energetic)

```

 ██  ██
 █▓  ▓█

█      █
 █    █
  ████

```

### Thinking Face
**Use Case**: Analyzing behavior, processing patterns
**Default Color**: Gray/White (neutral, contemplative)

```

  █  █
 █▓  ▓█


   ██


```

### Concerned Face
**Use Case**: User hasn't moved in a while, gentle reminder needed
**Default Color**: Yellow/Amber (caution, attention)

```

  █  █
  ▓  ▓


  ████


```

### Worried Face
**Use Case**: Extended inactivity, stronger reminder needed
**Default Color**: Orange/Red (urgent but caring)

```

 █    █
  █  █
  ▓  ▓

   ██
  █  █
 █    █
```

### Sleeping Face
**Use Case**: Night mode, user away, low activity period
**Default Color**: Blue/Purple (calm, restful)

```

 ██  ██



  ████


```

### Sleeping with ZZZ
**Use Case**: Deep sleep mode, extended inactivity accepted
**Default Color**: Blue/Purple with cyan accents

```
    ░░░
      ░
    ░░░
  ░░
   ░
  ░░
░░
 ░
```

## Icons & Symbols

### Heart
**Use Case**: Encouragement, self-care reminder, positive reinforcement
**Default Color**: Pink/Red (love, care)

```

 ██ ██
█▓▓█▓▓█
█▓▓▓▓▓█
 █▓▓▓█
  █▓█
   █

```

### Water Drop
**Use Case**: Hydration reminder
**Default Color**: Cyan/Blue (water, refreshment)

```
   █
  █▓█
 █▓▓▓█
 █▓░▓█
 █▓▓▓█
  █▓█
   █

```

### Checkmark
**Use Case**: Acknowledgment, task completed, good job
**Default Color**: Green (success, positive)

```

      █
     ██
    ██
██ ██
 ███
  █

```

### Exclamation Point
**Use Case**: Alert, important reminder, attention needed
**Default Color**: Orange/Red (alert, urgency)

```
   ██
   ██
   ██
   ██
   ██

   ██

```

### Walking Person
**Use Case**: Movement reminder, "take a walk"
**Default Color**: Green (healthy activity)

```
   ██
   ██
  ████
   ██
  ██
   █
    █

```

### Stretching Person
**Use Case**: Stretch reminder, "stretch it out"
**Default Color**: Green (healthy activity)

```
  ████
   ██
   ██
  ████
   ██
  █  █
 █    █

```

### Sparkle
**Use Case**: Celebration, achievement, positive moment
**Default Color**: Yellow/Multi-color (joy, celebration)

```
   █

  █▓█
█  ▓  █
  █▓█

   █

```

### Question Mark
**Use Case**: Uncertainty, checking in, "are you there?"
**Default Color**: Yellow (inquiry, curiosity)

```
  ███
 █   █
     █
    █
   █

   █

```

## Color Palettes

### Emotional Color Mapping

| Emotion | Primary RGB | Use Case |
|---------|-------------|----------|
| Happy | `(0, 50, 0)` Green | Positive state, healthy behavior |
| Celebrating | `(50, 50, 0)` Yellow | Achievement, celebration |
| Concerned | `(40, 40, 0)` Yellow | Mild attention needed |
| Worried | `(50, 15, 0)` Orange | Stronger reminder needed |
| Sleeping | `(0, 0, 30)` Blue | Rest mode, night mode |
| Hydration | `(0, 30, 50)` Cyan | Water reminder |
| Love/Care | `(50, 0, 20)` Pink | Encouragement, care |
| Success | `(0, 50, 10)` Bright Green | Task completed |
| Alert | `(50, 20, 0)` Orange-Red | Important attention |

## Animation Patterns

### Breathing Effect
A gentle pulsing animation that makes the pattern "breathe" by varying brightness.

**Duration**: 3 seconds per cycle
**Use**: Calm, peaceful states (happy, sleeping, concerned)
**Effect**: Smooth sine wave brightness variation

### Static Display
Pattern shown at constant brightness.

**Duration**: 2 seconds typically
**Use**: Quick messages, icons, alerts
**Effect**: Immediate, clear communication

### Color Cycling
Pattern colors change through a spectrum.

**Duration**: 4-6 seconds
**Use**: Celebration, very happy states
**Effect**: Dynamic, joyful

## Usage in Code

### Display a Simple Pattern

```python
from personality.pixel_art import HAPPY_FACE, ColorPalette
from personality.pixel_art import get_colored_pattern

# Get colored version
colored_pattern = get_colored_pattern(HAPPY_FACE, ColorPalette.HAPPY)

# Display on matrix (your display code here)
```

### Create Custom Pattern

```python
# Define your own 8x8 pattern
CUSTOM_PATTERN = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 2, 0, 0, 2, 0, 1],  # Eyes
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],  # Smile
    [1, 0, 0, 1, 1, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
]

# Apply colors
custom_palette = {
    0: (0, 0, 0),      # Background
    1: (30, 0, 30),    # Purple outline
    2: (50, 50, 0),    # Yellow details
}

colored = get_colored_pattern(CUSTOM_PATTERN, custom_palette)
```

### Test Patterns in Console

```bash
# Visualize all patterns (no hardware needed)
python examples/pattern_demo.py --console

# List available patterns
python examples/pattern_demo.py --list
```

### Test on Hardware

```bash
# Display all patterns sequentially
sudo python examples/pattern_demo.py

# Display specific pattern
sudo python examples/pattern_demo.py --pattern happy
```

## Design Guidelines

### Creating New Patterns

**Readability at 8x8 Resolution:**
- Use simple, bold shapes
- Minimum 2 pixels for fine details
- Test visibility from 1-2 meters distance

**Color Selection:**
- Limit to 2-3 colors per pattern for clarity
- Use contrasting colors for visibility
- Consider brightness (50-80 recommended for comfort)

**Emotional Design:**
- Happy: rounded shapes, upward curves
- Sad/Worried: downward curves, drooping features
- Alert: angular shapes, sharp points
- Calm: soft curves, symmetry

### Pattern Naming Convention

- **Expressions**: Describe emotion (e.g., `happy`, `worried`)
- **Icons**: Describe object/action (e.g., `heart`, `water`)
- **Actions**: Use verb form (e.g., `walking`, `stretching`)

## Future Expansions

### Planned Additions
- **Numbers**: 0-9 for countdowns
- **Letters**: Simple alphabet for messages
- **Weather Icons**: Sun, cloud, rain
- **Progress Bars**: Visual task completion
- **Arrows**: Directional indicators

### Animation Ideas
- **Winking**: Playful interaction
- **Blinking**: More lifelike expressions
- **Scrolling Text**: Short messages
- **Transitions**: Smooth morphing between expressions

## Contributing New Patterns

Want to add new patterns? See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

**Submit your designs:**
1. Create pattern in `src/personality/pixel_art.py`
2. Add visualization to this document
3. Test on hardware or console
4. Submit pull request with screenshots/photos

---

**Let your Pixel Plant express itself!** 🌿✨

*Last updated: December 2024*
