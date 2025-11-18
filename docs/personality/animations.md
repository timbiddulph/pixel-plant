# Pixel Rise & Fall Animations

## Overview

Inspired by the pixel plant in Becky Chambers' novel *"The Long Way to a Small, Angry Planet"*, where pixels physically rise up from the base to form images, the Pixel Plant includes beautiful rise and fall animations for all pattern transitions.

> *"The pixels lifted up from the base into place to make the image"*

This creates an organic, living feel that makes your Pixel Plant companion feel more alive and caring.

## How It Works

When changing from one pattern to another:

1. **Fall Animation**: Current pixels gradually "fall" back down to the base
2. **Brief Pause**: Empty state at the base (pixels resting)
3. **Rise Animation**: New pixels "rise up" from the base to form the new pattern

This creates a smooth, natural transition that feels mechanical yet organic—perfectly fitting the caring companion aesthetic.

## Animation Styles

### 🌊 Cascade (Default)
**Description**: Pixels rise based on their final row position
**Effect**: Bottom rows rise first, top rows rise last—like water flowing upward
**Best For**: Most organic feel, recommended default

**Timing**:
- Bottom pixels (row 7) start rising immediately
- Top pixels (row 0) start rising slightly later
- Creates a cascading wave effect

**Code**:
```python
animator.transition(old_pattern, new_pattern, style='cascade')
```

### 〰️ Wave
**Description**: Pixels rise column by column from left to right
**Effect**: A wave sweeps across the display building the image
**Best For**: Dramatic reveals, directional emphasis

**Timing**:
- Column 0 (left) rises completely first
- Column 1 rises next, etc.
- Creates a left-to-right scanning effect

**Code**:
```python
animator.transition(old_pattern, new_pattern, style='wave')
```

### ⏫ Synchronized
**Description**: All pixels rise together uniformly
**Effect**: The entire image materializes from bottom to top
**Best For**: Quick transitions, minimalist aesthetic

**Timing**:
- All pixels at the same row rise simultaneously
- Simple, clean effect
- Fastest to understand

**Code**:
```python
animator.transition(old_pattern, new_pattern, style='synchronized')
```

## Usage Examples

### Basic Animation

```python
from personality.pixel_art import HAPPY_FACE, HEART
from personality.animations import PixelAnimator

animator = PixelAnimator()

# Rise from nothing to happy face
for frame in animator.transition(None, HAPPY_FACE, style='cascade'):
    display_on_matrix(frame)

# Transition from happy to heart
for frame in animator.transition(HAPPY_FACE, HEART, style='cascade'):
    display_on_matrix(frame)
```

### Adjusting Speed

```python
# Faster animation
for frame in animator.transition(
    old_pattern,
    new_pattern,
    style='cascade',
    fall_steps=5,   # Fewer steps = faster fall
    rise_steps=6    # Fewer steps = faster rise
):
    display_on_matrix(frame)

# Slower, more dramatic animation
for frame in animator.transition(
    old_pattern,
    new_pattern,
    style='wave',
    fall_steps=12,  # More steps = slower fall
    rise_steps=15   # More steps = slower rise
):
    display_on_matrix(frame)
```

### Console Testing

```bash
# Test all three styles
python examples/quick_animation_test.py

# Full demo with cascade
python examples/pattern_demo.py --console --animate --style cascade

# Full demo with wave
python examples/pattern_demo.py --console --animate --style wave

# Full demo with synchronized
python examples/pattern_demo.py --console --animate --style synchronized
```

## Animation Module Reference

### PixelAnimator Class

```python
class PixelAnimator:
    def __init__(self, width=8, height=8)
```

Creates an animator for 8x8 patterns.

#### Methods

**`rise_cascade(pattern, steps=12, delay=0.04)`**
- Animate pixels rising in cascade style
- Returns: Generator yielding intermediate frames

**`rise_wave(pattern, steps=8, delay=0.05)`**
- Animate pixels rising column by column
- Returns: Generator yielding intermediate frames

**`rise_synchronized(pattern, steps=10, delay=0.06)`**
- Animate all pixels rising uniformly
- Returns: Generator yielding intermediate frames

**`fall_cascade(pattern, steps=10, delay=0.04)`**
- Animate pixels falling in cascade style
- Returns: Generator yielding intermediate frames

**`fall_synchronized(pattern, steps=8, delay=0.05)`**
- Animate all pixels falling uniformly
- Returns: Generator yielding intermediate frames

**`transition(from_pattern, to_pattern, style='cascade', fall_steps=8, rise_steps=10)`**
- Complete transition: fall old pattern → rise new pattern
- `from_pattern`: Current pattern (or None for first display)
- `to_pattern`: Target pattern to display
- `style`: 'cascade', 'wave', or 'synchronized'
- `fall_steps`: Animation steps for falling
- `rise_steps`: Animation steps for rising
- Returns: Generator yielding all intermediate frames

## Performance Considerations

### Frame Rate

Each animation step includes a small delay (0.04-0.06 seconds) for visibility:

- **Cascade**: ~12 steps rise = ~0.5 seconds
- **Wave**: ~8 steps × 8 columns = ~3.2 seconds
- **Synchronized**: ~10 steps = ~0.6 seconds

Adjust `steps` and `delay` parameters to match your performance needs.

### Memory Usage

Animations generate intermediate frames as needed using Python generators:
- **Memory efficient**: Only one frame in memory at a time
- **Streaming**: Frames generated on-demand
- **No storage**: Intermediate states not saved

### Hardware Performance

On Raspberry Pi Zero 2 W:
- Animation calculation: <5ms per frame (negligible)
- LED update: ~1-2ms for 64 LEDs
- Network latency: None (all local)

**Bottleneck**: Display refresh rate, not computation

## Integration with Pixel Plant

### Mood Changes

When the plant's mood changes:

```python
# Plant becomes concerned
animator.transition(
    current_mood_pattern,
    CONCERNED_FACE,
    style='cascade'
)
```

### Message Display

When showing icons/reminders:

```python
# Show hydration reminder
animator.transition(
    CONCERNED_FACE,
    WATER_DROP,
    style='wave'  # Wave for attention
)
```

### Sleep Mode

Gentle transition to rest:

```python
# Going to sleep
animator.transition(
    HAPPY_FACE,
    SLEEPING_FACE,
    style='synchronized',  # Calm, uniform
    fall_steps=15,         # Slow, peaceful
    rise_steps=15
)
```

## Design Philosophy

The rise and fall animations embody the Pixel Plant's core philosophy:

- **Organic Motion**: Despite being digital, movements feel natural
- **Caring Presence**: Transitions are gentle, never jarring
- **Living Companion**: The plant "assembles" itself, feeling alive
- **Becky Chambers' Vision**: Faithful to the literary inspiration

The animations transform the LED matrix from a static display into a living, breathing companion.

## Troubleshooting

**Animation too fast**:
- Increase `steps` parameter
- Increase `delay` in animation method source

**Animation too slow**:
- Decrease `steps` parameter
- Use 'synchronized' instead of 'wave'

**Choppy animation**:
- Check CPU usage (should be <10%)
- Reduce other background processes
- Verify power supply stability

**Pixels in wrong positions**:
- Verify LED matrix layout (serpentine vs progressive)
- Check `xy_to_index()` function matches your hardware

## Future Enhancements

Planned animation additions:

- **Breathing while static**: Gentle pulsing when displaying pattern
- **Sparkle effects**: Pixels twinkle during celebration
- **Ripple**: Waves emanating from center
- **Bounce**: Playful bouncing pixels
- **Custom paths**: Non-linear rise/fall trajectories

---

**Watch your Pixel Plant come alive!** 🌿✨

*Last updated: December 2024*
