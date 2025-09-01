/*
 * Pixel Plant LED Animation Manager
 * 
 * Manages all LED animations and visual expressions that bring the Pixel Plant's
 * personality to life. Creates caring, organic animations that feel natural and
 * supportive rather than robotic or harsh.
 */

#ifndef LED_MANAGER_H
#define LED_MANAGER_H

#include <Arduino.h>
#include <FastLED.h>
#include "../utils/logger.h"
#include "../../config.h"

// Animation types for different personality expressions
enum AnimationType {
  ANIM_NONE = 0,
  ANIM_BREATHING,           // Gentle breathing for normal states
  ANIM_SPARKLE,            // Happy sparkles
  ANIM_PULSE,              // Caring pulse
  ANIM_WAVE,               // Gentle attention wave
  ANIM_RAINBOW,            // Celebration rainbow
  ANIM_GROWING,            // Growing plant animation
  ANIM_CARING,             // Warm caring glow
  ANIM_CONCERNED,          // Concerned pulsing
  ANIM_URGENT,             // Urgent but not harsh attention
  ANIM_SLEEPING,           // Peaceful sleeping animation
  ANIM_WAKEUP,             // Gentle wakeup sequence
  ANIM_STARTUP,            // System startup animation
  ANIM_ERROR,              // Error state (still gentle)
  ANIM_CUSTOM,             // Custom animation
  ANIM_COUNT
};

// Color themes for different moods
struct ColorTheme {
  CRGB primary;
  CRGB secondary;
  CRGB accent;
  uint8_t brightness;
  String name;
};

// Animation state for complex animations
struct AnimationState {
  AnimationType currentType;
  unsigned long startTime;
  unsigned long duration;
  float phase;                  // 0.0 - 1.0 animation progress
  float speed;                  // Animation speed multiplier
  bool isLooping;
  bool isActive;
  
  // Animation parameters
  float intensity;              // 0.0 - 1.0 animation intensity
  uint8_t brightness;           // 0 - 255 brightness level
  int centerPosition;           // Center LED for radial effects
  int waveLength;              // For wave-based animations
  
  // Color parameters
  CRGB primaryColor;
  CRGB secondaryColor;
  uint8_t hue;
  uint8_t saturation;
};

class LEDManager {
private:
  // FastLED setup
  CRGB* leds;
  int ledCount;
  uint8_t globalBrightness;
  
  // Animation state
  AnimationState currentAnimation;
  AnimationType queuedAnimation;
  MoodType currentMood;
  
  // Color themes for different moods
  ColorTheme moodThemes[MOOD_COUNT];
  
  // Animation timing
  unsigned long lastUpdate;
  unsigned long updateInterval;
  
  // Personality parameters
  float personalityWarmth;      // How warm/friendly colors should be
  float energyLevel;            // How energetic animations should be
  bool gentleMode;              // Extra gentle animations for sensitive users
  
  // Effects state
  struct {
    float breathingPhase;
    float sparkleTimer;
    int wavePosition;
    float pulseIntensity;
    unsigned long effectStartTime;
    std::vector<int> sparklePositions;
  } effectState;
  
  // Color management
  void initializeColorThemes();
  ColorTheme getCurrentTheme() const;
  CRGB blendColors(CRGB color1, CRGB color2, float ratio);
  CRGB adjustColorWarmth(CRGB color, float warmth);
  
  // Core animation implementations
  void renderBreathingAnimation();
  void renderSparkleAnimation();
  void renderPulseAnimation();
  void renderWaveAnimation();
  void renderRainbowAnimation();
  void renderGrowingAnimation();
  void renderCaringAnimation();
  void renderConcernedAnimation();
  void renderUrgentAnimation();
  void renderSleepingAnimation();
  void renderWakeupAnimation();
  void renderStartupAnimation();
  void renderErrorAnimation();
  
  // Animation helpers
  void clearLEDs();
  void setAllLEDs(CRGB color);
  void setLEDRange(int start, int end, CRGB color);
  void fadeLEDRange(int start, int end, uint8_t fadeAmount);
  void applyGlobalBrightness();
  
  // Organic animation helpers
  float smoothStep(float t);              // Smooth interpolation
  float organicPulse(float phase);        // Natural pulse curve
  float gentleWave(float phase, float frequency);
  CRGB warmGlow(CRGB baseColor, float intensity);
  
public:
  LEDManager();
  ~LEDManager();
  
  // Initialization
  bool initialize(int ledCount = LED_COUNT, int dataPin = LED_DATA_PIN);
  void setPersonalityTraits(float warmth, float energy);
  void setGentleMode(bool enabled) { gentleMode = enabled; }
  
  // Main update cycle
  void update();
  void show() { FastLED.show(); }
  
  // Animation control
  void startAnimation(AnimationType type, MoodType mood = MOOD_HAPPY);
  void startAnimation(AnimationType type, unsigned long duration, MoodType mood = MOOD_HAPPY);
  void queueAnimation(AnimationType type, MoodType mood = MOOD_HAPPY);
  void stopAnimation();
  bool isAnimationActive() const { return currentAnimation.isActive; }
  
  // Mood-based animations (primary interface)
  void showMoodDisplay(MoodType mood);
  void showStartupAnimation();
  void showCaringAnimation();
  void showConcernedAnimation();
  void showWakeupAnimation();
  void showSleepingAnimation();
  void showCelebrationAnimation();
  void showMessageAnimation();
  void showErrorPattern();
  
  // Brightness and color control
  void setBrightness(uint8_t brightness);
  uint8_t getBrightness() const { return globalBrightness; }
  void adjustBrightness(int delta);
  void setMoodColors(MoodType mood);
  
  // Special effects
  void flashColor(CRGB color, int flashCount = 3);
  void breatheColor(CRGB color, float speed = 1.0);
  void sparkleEffect(CRGB color, int sparkleCount = 5);
  void waveEffect(CRGB color, float speed = 1.0);
  
  // Interactive animations
  void showAttentionGetter(bool urgent = false);
  void showPositiveFeedback();
  void showGentleReminder();
  void showAppreciation();
  
  // Organic behavior simulation
  void simulateNaturalBehavior();     // Subtle organic movements
  void showLifelikePulse();           // Heartbeat-like pulse
  void mimicPlantGrowth();            // Growing plant animation
  
  // Time-based automatic behaviors
  void updateForTimeOfDay(int hour);
  void adjustForAmbientLight(float lightLevel);
  void respondToUserActivity(bool active);
  
  // Customization
  void setCustomColor(CRGB color);
  void setCustomTheme(ColorTheme theme);
  void setAnimationSpeed(float speedMultiplier);
  void setAnimationIntensity(float intensity);
  
  // Test and calibration
  void runTestPattern();
  void runColorCalibration();
  void showPixelByPixelTest();
  void validateConnections();
  
  // Caring philosophy implementations
  void showGentleCare();              // Soft, caring presence
  void showPatientWaiting();          // Patient, understanding animation
  void showQuietSupport();            // Subtle supportive presence
  void showCelebrationJoy();          // Joyful but not overwhelming
  
  // Advanced features
  void setReactiveMode(bool enabled); // React to sound/movement
  void setBreathingRate(float rate);  // Adjust breathing animation speed
  void synchronizeWithAudio(bool enabled); // Sync with audio output
  
  // Status and diagnostics
  String getStatusString() const;
  bool selfTest();
  void printAnimationState() const;
  
  // Energy saving
  void setEcoMode(bool enabled);      // Reduce power consumption
  void dimForNight(bool enabled);     // Automatic nighttime dimming
};

// Helper functions for animation mathematics
namespace AnimationMath {
  float easeInOut(float t);           // Smooth ease in/out curve
  float bounce(float t);              // Gentle bounce effect
  float organic(float t, float variation); // Natural, organic movement
  CRGB interpolateHSV(CRGB color1, CRGB color2, float t);
  float perlinNoise(float x, float y = 0); // Organic variation
}

// Predefined color palettes for different times and moods
namespace ColorPalettes {
  extern const ColorTheme CARING_WARMTH;
  extern const ColorTheme GENTLE_CONCERN;
  extern const ColorTheme PEACEFUL_SLEEP;
  extern const ColorTheme JOYFUL_CELEBRATION;
  extern const ColorTheme NATURAL_EARTH;
  extern const ColorTheme SOFT_SUNSET;
  extern const ColorTheme MORNING_DEW;
  extern const ColorTheme CALMING_OCEAN;
}

// Animation presets for common caring scenarios
namespace CaringAnimations {
  void showFirstTimeGreeting(LEDManager& led);
  void showDailyCheckIn(LEDManager& led);
  void showHealthReminder(LEDManager& led, const String& reminderType);
  void showUserAppreciation(LEDManager& led);
  void showGentleGoodbye(LEDManager& led);
  void showCompassionateSupport(LEDManager& led);
}

#endif // LED_MANAGER_H