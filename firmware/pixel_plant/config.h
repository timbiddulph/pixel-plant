/*
 * Pixel Plant Configuration
 * Hardware pins, system constants, and tunable parameters
 */

#ifndef CONFIG_H
#define CONFIG_H

// ============================================================================
// FIRMWARE VERSION
// ============================================================================
#define FIRMWARE_VERSION "1.0.0-alpha"
#define BUILD_DATE __DATE__
#define BUILD_TIME __TIME__

// ============================================================================
// HARDWARE PIN ASSIGNMENTS (ESP32-S3 FireBeetle)
// ============================================================================

// LED Strip (WS2812B)
#define LED_DATA_PIN      18
#define LED_COUNT         60
#define LED_BRIGHTNESS    50    // 0-255, start conservative

// I2S Audio (MAX98357A)
#define AUDIO_BCLK_PIN    19    // Bit clock
#define AUDIO_LRC_PIN     20    // Left/Right clock
#define AUDIO_DIN_PIN     21    // Data input

// Sensors
#define PIR_SENSOR_PIN    22    // Motion detection
#define CAMERA_POWER_PIN  23    // Camera power control (if needed)

// System LEDs (built-in)
#define STATUS_LED_PIN    2     // Built-in status LED

// ============================================================================
// SYSTEM TIMING
// ============================================================================
#define SERIAL_BAUD_RATE        115200
#define UPDATE_INTERVAL         100     // Main loop update (ms)
#define HEARTBEAT_INTERVAL      10000   // System heartbeat (ms)
#define REMINDER_CHECK_INTERVAL 60000   // Check for reminders (ms)

// ============================================================================
// BEHAVIOR MONITORING
// ============================================================================

// Activity thresholds (minutes)
#define NORMAL_INACTIVITY_THRESHOLD   30    // When to start caring
#define CONCERNED_INACTIVITY_THRESHOLD 60   // When to be more concerned
#define URGENT_INACTIVITY_THRESHOLD   120   // When to be worried

// Reminder intervals (minutes)
#define HYDRATION_REMINDER_INTERVAL   45    // Remind to drink water
#define MOVEMENT_REMINDER_INTERVAL    60    // Remind to move/stretch
#define POSTURE_REMINDER_INTERVAL     30    // Remind about posture

// Detection sensitivity
#define MOTION_SENSITIVITY        HIGH     // PIR sensor sensitivity
#define CAMERA_MOTION_THRESHOLD   50       // Computer vision motion threshold

// ============================================================================
// PERSONALITY SYSTEM
// ============================================================================

// Mood states
enum MoodType {
  MOOD_HAPPY = 0,
  MOOD_CARING,
  MOOD_CONCERNED,
  MOOD_WORRIED,
  MOOD_SLEEPING,
  MOOD_CELEBRATING,
  MOOD_COUNT
};

// System states
enum SystemState {
  SYSTEM_INITIALIZING = 0,
  SYSTEM_READY,
  SYSTEM_CARING,
  SYSTEM_CONCERNED,
  SYSTEM_SLEEPING,
  SYSTEM_ERROR,
  SYSTEM_UPDATING
};

// Response variety
#define MAX_RESPONSE_VARIATIONS   10    // Different ways to say the same thing
#define RESPONSE_COOLDOWN         5000  // Minimum time between responses (ms)

// ============================================================================
// LED ANIMATIONS
// ============================================================================

// Color definitions (RGB)
#define COLOR_HAPPY       0x00FF00    // Green
#define COLOR_CARING      0xFFFF00    // Yellow
#define COLOR_CONCERNED   0xFF8800    // Orange
#define COLOR_WORRIED     0xFF0000    // Red
#define COLOR_SLEEPING    0x000088    // Blue
#define COLOR_CELEBRATING 0xFF00FF    // Purple

// Animation timing
#define BREATHING_SPEED       2000    // Breathing animation period (ms)
#define SPARKLE_FREQUENCY     100     // How often sparkles appear (ms)
#define FADE_SPEED           20       // Color transition speed (ms)

// Pattern parameters
#define STARTUP_ANIMATION_TIME  3000  // How long startup animation runs (ms)
#define CARING_ANIMATION_TIME   5000  // How long caring animation runs (ms)
#define ERROR_BLINK_RATE        500   // Error pattern blink rate (ms)

// ============================================================================
// AUDIO SYSTEM
// ============================================================================

// Volume levels (0.0 - 1.0)
#define AUDIO_VOLUME_DEFAULT      0.7
#define AUDIO_VOLUME_QUIET        0.3
#define AUDIO_VOLUME_URGENT       1.0

// Speech synthesis
#define SPEECH_RATE_DEFAULT       150   // Words per minute
#define SPEECH_PITCH_DEFAULT      50    // Voice pitch (0-100)

// Audio file settings
#define AUDIO_SAMPLE_RATE         22050
#define AUDIO_BITS_PER_SAMPLE     16
#define AUDIO_CHANNELS            1     // Mono

// ============================================================================
// AI/COMPUTER VISION
// ============================================================================

// TensorFlow Lite settings
#define TFLITE_ARENA_SIZE         200 * 1024  // 200KB for ML models
#define INFERENCE_INTERVAL        1000         // How often to run inference (ms)

// Camera settings
#define CAMERA_FRAME_SIZE         FRAMESIZE_QVGA  // 320x240
#define CAMERA_QUALITY            12              // JPEG quality (0-63)
#define CAMERA_BRIGHTNESS         0               // -2 to +2

// Behavioral detection
#define SITTING_CONFIDENCE_THRESHOLD    0.7   // Confidence for "sitting" detection
#define STANDING_CONFIDENCE_THRESHOLD   0.7   // Confidence for "standing" detection
#define FACE_DETECTION_THRESHOLD        0.6   // Face detection confidence

// ============================================================================
// SYSTEM LIMITS
// ============================================================================

// Safety thresholds
#define MAX_OPERATING_TEMP        75      // °C - thermal shutdown temperature
#define MIN_FREE_MEMORY          10000    // Bytes - minimum free heap
#define WATCHDOG_TIMEOUT         30       // Seconds before system reset

// Storage limits
#define MAX_LOG_ENTRIES          100      // Maximum log entries to keep
#define MAX_BEHAVIOR_HISTORY     1000     // Behavior data points to store
#define CONFIG_SAVE_INTERVAL     300000   // Auto-save config every 5 minutes (ms)

// Network settings
#define WIFI_CONNECT_TIMEOUT     20000    // WiFi connection timeout (ms)
#define HTTP_REQUEST_TIMEOUT     5000     // HTTP request timeout (ms)
#define UPDATE_CHECK_INTERVAL    86400000 // Check for updates daily (ms)

// ============================================================================
// USER CUSTOMIZATION
// ============================================================================

// Default schedule (24-hour format)
#define DEFAULT_WORK_START_HOUR   9
#define DEFAULT_WORK_END_HOUR     17
#define DEFAULT_LUNCH_HOUR        12
#define DEFAULT_LUNCH_DURATION    60     // minutes

// Personalization
#define DEFAULT_USER_NAME         "friend"
#define DEFAULT_CARE_LEVEL        5      // 1-10 scale of how caring to be
#define DEFAULT_REMINDER_STYLE    GENTLE // GENTLE, PERSISTENT, URGENT

// Learning parameters
#define LEARNING_RATE             0.1    // How quickly to adapt to user patterns
#define PATTERN_CONFIDENCE_MIN    0.8    // Minimum confidence to act on learned patterns
#define ADAPTATION_PERIOD_DAYS    7      // Days to learn user patterns

// ============================================================================
// DEBUG AND DEVELOPMENT
// ============================================================================

// Debug levels
#define DEBUG_NONE     0
#define DEBUG_ERROR    1
#define DEBUG_WARNING  2
#define DEBUG_INFO     3
#define DEBUG_VERBOSE  4

// Current debug level (change for different verbosity)
#define DEBUG_LEVEL    DEBUG_INFO

// Debug features
#define ENABLE_SERIAL_DEBUG       true
#define ENABLE_PERFORMANCE_TIMING true
#define ENABLE_MEMORY_MONITORING  true

// Development flags
#define DEVELOPMENT_MODE          true   // Enable extra debugging features
#define SIMULATION_MODE           false  // Run without hardware (for testing)
#define FAST_BOOT_MODE           false  // Skip some initialization for faster development

// ============================================================================
// CARING PHILOSOPHY CONSTANTS
// ============================================================================

// Core caring principles embedded in configuration
#define CARING_RESPONSE_WARMTH        0.9    // How warm/friendly responses should be
#define PERSISTENCE_WITHOUT_NAGGING   0.7    // Balance of helpful vs annoying
#define EMOTIONAL_INTELLIGENCE_LEVEL  0.8    // How well we read user mood
#define CELEBRATION_ENTHUSIASM        0.9    // How much we celebrate user success

// These values influence the personality engine's behavior generation

#endif // CONFIG_H