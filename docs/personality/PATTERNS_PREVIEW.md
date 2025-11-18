# 8x8 Pixel Art Patterns - Visual Preview

Quick visual reference of all available patterns for the Pixel Plant LED matrix.

## Emotional Expressions (7 patterns)

### Happy
```
  █  █
  ▓  ▓

 █    █
  █  █
   ██
```
*Classic smile - your plant is content!*

### Very Happy
```
 ██  ██
 █▓  ▓█

█      █
 █    █
  ████
```
*Big celebration smile - you did great!*

### Thinking
```
  █  █
 █▓  ▓█


   ██
```
*Contemplative - analyzing your patterns*

### Concerned
```
  █  █
  ▓  ▓


  ████
```
*Neutral expression - gentle reminder time*

### Worried
```
 █    █
  █  █
  ▓  ▓

   ██
  █  █
 █    █
```
*Frowning - you really need to take care!*

### Sleeping
```
 ██  ██



  ████
```
*Peaceful rest - night mode*

### Sleeping ZZZ
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
*Animation for sleep mode*

## Icons & Symbols (8 patterns)

### Heart ❤️
```
 ██ ██
█▓▓█▓▓█
█▓▓▓▓▓█
 █▓▓▓█
  █▓█
   █
```
*Self-care and encouragement*

### Water Drop 💧
```
   █
  █▓█
 █▓▓▓█
 █▓░▓█
 █▓▓▓█
  █▓█
   █
```
*Hydration reminder*

### Checkmark ✓
```
      █
     ██
    ██
██ ██
 ███
  █
```
*Good job! Acknowledged!*

### Exclamation ❗
```
   ██
   ██
   ██
   ██
   ██

   ██
```
*Important reminder needed*

### Walking Person 🚶
```
   ██
   ██
  ████
   ██
  ██
   █
    █
```
*Time to take a walk!*

### Stretching Person 🤸
```
  ████
   ██
   ██
  ████
   ██
  █  █
 █    █
```
*Stretch it out!*

### Sparkle ✨
```
   █

  █▓█
█  ▓  █
  █▓█

   █
```
*Celebration and joy*

### Question Mark ❓
```
  ███
 █   █
     █
    █
   █

   █
```
*Are you there?*

---

## Color Combinations

Each pattern can be displayed in different color palettes:

| Palette | Primary Color | Use Case |
|---------|---------------|----------|
| Happy | Green | Normal, healthy state |
| Celebrating | Yellow | Achievement, joy |
| Concerned | Yellow/Amber | Gentle attention |
| Worried | Orange/Red | Urgent care |
| Sleeping | Blue/Purple | Rest mode |
| Hydration | Cyan | Water reminders |
| Love | Pink/Red | Encouragement |
| Success | Bright Green | Completed tasks |
| Alert | Orange-Red | Alerts |

## Testing Patterns

### Without Hardware (Console)
```bash
python examples/pattern_demo.py --console
```

### With LED Matrix
```bash
sudo python examples/pattern_demo.py
sudo python examples/pattern_demo.py --pattern happy
```

## Creating Your Own

Edit `src/personality/pixel_art.py` to add new patterns:

```python
MY_CUSTOM_FACE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],  # Eyes
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],  # Custom expression
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
```

Where:
- `0` = off (background)
- `1` = primary color
- `2` = secondary color
- `3` = accent color

---

**Total Patterns**: 15 (7 expressions + 8 icons)
**Ready to use**: ✅ All patterns tested and documented

*Give your Pixel Plant a personality!* 🌿✨
