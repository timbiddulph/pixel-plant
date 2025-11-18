# Rise & Fall Animation Preview

> *"The pixels lifted up from the base into place to make the image"*
> — Inspired by Becky Chambers' *The Long Way to a Small, Angry Planet*

## What Are Rise/Fall Animations?

When your Pixel Plant changes expressions or shows new messages, pixels don't just instantly change—they **rise up from the base** to form the new pattern, creating an organic, living feel.

## Animation Sequence

### 1. Current Pattern (e.g., Happy Face)
```
  █  █
  ▓  ▓

 █    █
  █  █
   ██
```

### 2. Fall Animation (pixels descend)
```
Frame 1:              Frame 2:              Frame 3:

  █  █
  ▓  ▓                  ▓  ▓                  ▓  ▓
                        █  █
 █    █                 █  █                  █  █
  █  █                   ██                   ██
   ██                                       █    █
```

### 3. Empty Base (brief pause)
```




```

### 4. Rise Animation (new pattern ascends)
```
Frame 1:              Frame 2:              Frame 3:



                         ░

                         ▓
   █                    █▓█                  █▓▓▓█
                        █▓█                  █▓░▓█
```

### 5. Final Pattern (Water Drop)
```
   █
  █▓█
 █▓▓▓█
 █▓░▓█
 █▓▓▓█
  █▓█
   █
```

## Animation Styles Compared

### 🌊 Cascade (Recommended)
**Effect**: Bottom pixels rise first, creating an upward flow

```
Step 1:  Step 2:  Step 3:  Step 4:  Step 5:







   ██      ██      ██      ██      ██
         █  █    █  █    █  █    █  █
                ▓  ▓    ▓  ▓    ▓  ▓
               █    █  █    █  █    █
```

**Best for**: Natural, organic feel (default recommended)

### 〰️ Wave
**Effect**: Columns rise left to right sequentially

```
Col 0:   Col 1:   Col 2:   Col 3:   ...








█        ██       ██ █     ██ █▓    ...
▓        ▓▓       ▓▓ ▓     ▓▓ ▓▓    ...
█        ██       ██ █     ██ █     ...
```

**Best for**: Dramatic reveals, scanning effect

### ⏫ Synchronized
**Effect**: All pixels at same row rise together

```
Step 1:  Step 2:  Step 3:  Step 4:







  ████    ████    ████    ████
  █  █   ██  █   █ ██ █   █ ██ █
         ▓    ▓  ▓  ▓  ▓  ▓  ▓  ▓
```

**Best for**: Quick, clean transitions

## Real-World Example Transitions

### 😊 Happy → 💧 Water Drop Reminder
```
CASCADE STYLE:

1. Happy face shown
2. Eyes disappear (fall)
3. Smile disappears (fall)
4. Brief empty moment
5. Bottom of water drop rises
6. Middle section rises
7. Top drop rises
8. Sparkle appears
9. Complete!

Total time: ~1.2 seconds
```

### 💧 Water → ❤️ Heart Encouragement
```
WAVE STYLE:

1. Water drop shown
2. Left column falls
3. Next column falls...
4. All columns fallen
5. Brief empty moment
6. Left column rises (heart shape)
7. Next column rises...
8. Full heart formed

Total time: ~2.5 seconds
```

### ❤️ Heart → 😊 Back to Happy
```
SYNCHRONIZED STYLE:

1. Heart shown
2. Top row disappears
3. Next row disappears...
4. All fallen
5. Brief pause
6. Bottom row rises (smile)
7. Next row rises...
8. Happy face complete

Total time: ~1.0 seconds
```

## Testing Animations

### Console (No Hardware Needed)

```bash
# Quick interactive test
python examples/quick_animation_test.py

# Full demo
python examples/pattern_demo.py --console --animate

# Try different styles
python examples/pattern_demo.py --console --animate --style cascade
python examples/pattern_demo.py --console --animate --style wave
python examples/pattern_demo.py --console --animate --style synchronized
```

### On LED Matrix

```bash
# (Hardware demo with animations coming soon!)
sudo python examples/pattern_demo.py --animate
```

## Animation Parameters

### Speed Control

```python
# Fast transition (urgent message)
animator.transition(old, new,
    style='synchronized',
    fall_steps=5,
    rise_steps=6
)
# ~0.7 seconds total

# Slow transition (going to sleep)
animator.transition(old, new,
    style='cascade',
    fall_steps=15,
    rise_steps=18
)
# ~2.0 seconds total
```

### Mood-Based Animation Selection

| Mood Change | Recommended Style | Speed | Why |
|-------------|------------------|-------|-----|
| Happy → Concerned | Cascade | Medium | Organic escalation |
| Concerned → Worried | Synchronized | Medium | Clear state change |
| Any → Sleeping | Cascade | Slow | Peaceful, calming |
| Sleeping → Awake | Synchronized | Fast | Alert, responsive |
| Any → Heart/Check | Wave | Medium | Attention-getting |
| Message → Message | Cascade | Fast | Quick updates |

## Why This Matters

The rise and fall animations aren't just aesthetic—they're core to the Pixel Plant philosophy:

### 🌿 Living Presence
Pixels assembling and disassembling make the plant feel **alive**, not just a static display

### 💚 Caring Transitions
Gentle, organic movements reflect the plant's **caring nature**—never harsh or jarring

### 📖 Literary Authenticity
Faithful to Becky Chambers' vision of technology that feels **magical yet mechanical**

### 🎭 Emotional Communication
Different animation styles can **amplify emotional context**:
- Cascade = natural, flowing care
- Wave = directed attention
- Synchronized = immediate, clear message

## Performance

**Frame Rate**: ~12-20 fps (animation smoothness)
**Transition Time**: 0.7-2.5 seconds (depending on style and parameters)
**CPU Usage**: <5% on Pi Zero 2 W
**Memory**: Negligible (generators used)

No performance impact on AI behavior monitoring!

## Future Enhancements

Planned additions:
- **Breathing**: Gentle pulsing while pattern is static
- **Bounce**: Playful bouncing pixels
- **Ripple**: Waves from center outward
- **Twinkle**: Sparkle effects for celebration
- **Custom paths**: Curved trajectories for rising pixels

---

**Experience the magic of pixels coming alive!** 🌿✨

*Last updated: December 2024*
