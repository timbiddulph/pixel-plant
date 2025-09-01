/*
 * Pixel Plant - LED Strip Test
 * 
 * Tests the WS2812B LED strip functionality
 * Verifies connections and basic animations
 * 
 * Hardware: ESP32-S3 + WS2812B LED Strip
 * Pin: GPIO 18 (configurable in config)
 */

#include <FastLED.h>

// LED Configuration
#define LED_PIN       18        // GPIO pin connected to LED data line
#define LED_COUNT     60        // Number of LEDs in strip (adjust to your strip)
#define BRIGHTNESS    50        // LED brightness (0-255)
#define LED_TYPE      WS2812B   // LED chip type
#define COLOR_ORDER   GRB       // Color order (depends on your strip)

// LED array
CRGB leds[LED_COUNT];

// Animation state
int currentTest = 0;
unsigned long lastTestChange = 0;
unsigned long testDuration = 5000; // Each test runs for 5 seconds

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n🌿 Pixel Plant LED Test Starting...");
  Serial.println("=====================================");
  Serial.printf("LED Count: %d\n", LED_COUNT);
  Serial.printf("LED Pin: GPIO %d\n", LED_PIN);
  Serial.printf("Brightness: %d/255\n", BRIGHTNESS);
  Serial.println("=====================================\n");
  
  // Initialize LED strip
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, LED_COUNT);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.clear();
  FastLED.show();
  
  Serial.println("✅ FastLED initialized successfully!");
  Serial.println("\nStarting LED tests...");
  Serial.println("Each test runs for 5 seconds");
  Serial.println("Tests will cycle automatically");
  Serial.println("=====================================\n");
  
  lastTestChange = millis();
}

void loop() {
  // Check if it's time to switch tests
  if (millis() - lastTestChange > testDuration) {
    currentTest = (currentTest + 1) % 8; // 8 different tests
    lastTestChange = millis();
    FastLED.clear();
    FastLED.show();
    delay(500); // Brief pause between tests
    printCurrentTest();
  }
  
  // Run current test
  switch (currentTest) {
    case 0:
      testBasicColors();
      break;
    case 1:
      testRainbow();
      break;
    case 2:
      testBreathing();
      break;
    case 3:
      testChase();
      break;
    case 4:
      testSparkle();
      break;
    case 5:
      testMoodColors();
      break;
    case 6:
      testPixelPlantAnimations();
      break;
    case 7:
      testIndividualLEDs();
      break;
  }
  
  FastLED.show();
  delay(50); // Smooth animation
}

void printCurrentTest() {
  Serial.print("Test ");
  Serial.print(currentTest + 1);
  Serial.print("/8: ");
  
  switch (currentTest) {
    case 0: Serial.println("Basic Colors (R-G-B-W)"); break;
    case 1: Serial.println("Rainbow Pattern"); break;
    case 2: Serial.println("Breathing Animation"); break;
    case 3: Serial.println("Chase Effect"); break;
    case 4: Serial.println("Sparkle Animation"); break;
    case 5: Serial.println("Mood Colors"); break;
    case 6: Serial.println("Pixel Plant Animations"); break;
    case 7: Serial.println("Individual LED Test"); break;
  }
}

void testBasicColors() {
  static int phase = 0;
  static unsigned long lastPhaseChange = 0;
  
  if (millis() - lastPhaseChange > 1000) { // Change color every second
    phase = (phase + 1) % 4;
    lastPhaseChange = millis();
  }
  
  CRGB color;
  switch (phase) {
    case 0: color = CRGB::Red; break;
    case 1: color = CRGB::Green; break;
    case 2: color = CRGB::Blue; break;
    case 3: color = CRGB::White; break;
  }
  
  fill_solid(leds, LED_COUNT, color);
}

void testRainbow() {
  static uint8_t startHue = 0;
  startHue += 2; // Speed of rainbow rotation
  
  fill_rainbow(leds, LED_COUNT, startHue, 255 / LED_COUNT);
}

void testBreathing() {
  static unsigned long breathStart = millis();
  float breathPhase = (millis() - breathStart) / 2000.0; // 2 second breathing cycle
  uint8_t brightness = (sin(breathPhase * 2 * PI) + 1) * 127; // 0-254 range
  
  fill_solid(leds, LED_COUNT, CRGB::Green);
  FastLED.setBrightness(brightness);
}

void testChase() {
  static int chasePos = 0;
  static unsigned long lastChaseMove = 0;
  
  if (millis() - lastChaseMove > 100) {
    chasePos = (chasePos + 1) % LED_COUNT;
    lastChaseMove = millis();
  }
  
  FastLED.setBrightness(BRIGHTNESS); // Reset brightness from breathing test
  fill_solid(leds, LED_COUNT, CRGB::Black);
  
  // Create a comet tail effect
  for (int i = 0; i < 5; i++) {
    int pos = (chasePos - i + LED_COUNT) % LED_COUNT;
    leds[pos] = CRGB::Blue;
    leds[pos].fadeToBlackBy(i * 50);
  }
}

void testSparkle() {
  static unsigned long lastSparkle = 0;
  
  if (millis() - lastSparkle > 100) {
    // Fade all LEDs slightly
    for (int i = 0; i < LED_COUNT; i++) {
      leds[i].fadeToBlackBy(20);
    }
    
    // Add new sparkle
    if (random(10) < 3) { // 30% chance of new sparkle
      int pos = random(LED_COUNT);
      leds[pos] = CRGB::White;
    }
    
    lastSparkle = millis();
  }
}

void testMoodColors() {
  static int mood = 0;
  static unsigned long lastMoodChange = 0;
  
  if (millis() - lastMoodChange > 1500) {
    mood = (mood + 1) % 5;
    lastMoodChange = millis();
  }
  
  CRGB color;
  switch (mood) {
    case 0: color = CRGB::Green;    break; // Happy
    case 1: color = CRGB::Yellow;   break; // Caring
    case 2: color = CRGB::Orange;   break; // Concerned
    case 3: color = CRGB::Red;      break; // Worried
    case 4: color = CRGB::Blue;     break; // Sleeping
  }
  
  // Gentle breathing with mood color
  float breathPhase = millis() / 1500.0;
  uint8_t brightness = (sin(breathPhase * 2 * PI) + 1) * 100 + 55; // 55-255 range
  
  fill_solid(leds, LED_COUNT, color);
  FastLED.setBrightness(brightness);
}

void testPixelPlantAnimations() {
  static int animation = 0;
  static unsigned long lastAnimChange = 0;
  
  if (millis() - lastAnimChange > 2000) {
    animation = (animation + 1) % 3;
    lastAnimChange = millis();
  }
  
  FastLED.setBrightness(BRIGHTNESS);
  
  switch (animation) {
    case 0:
      // "Growing" animation - like a plant growing
      growingAnimation();
      break;
    case 1:
      // "Caring" animation - warm pulsing
      caringAnimation();
      break;
    case 2:
      // "Alert" animation - gentle attention-getting
      alertAnimation();
      break;
  }
}

void growingAnimation() {
  static int growthPos = 0;
  static unsigned long lastGrowth = 0;
  
  if (millis() - lastGrowth > 100) {
    if (growthPos < LED_COUNT) {
      leds[growthPos] = CHSV(96, 255, 255); // Green hue
      growthPos++;
    } else {
      // Reset and fade
      for (int i = 0; i < LED_COUNT; i++) {
        leds[i].fadeToBlackBy(10);
      }
      if (leds[0].r + leds[0].g + leds[0].b < 10) {
        growthPos = 0; // Restart growth
      }
    }
    lastGrowth = millis();
  }
}

void caringAnimation() {
  // Warm, gentle pulsing in yellow/orange tones
  float pulsePhase = millis() / 1000.0;
  uint8_t brightness = (sin(pulsePhase * 2 * PI) + 1) * 100 + 50;
  
  CRGB warmColor = CHSV(32, 200, brightness); // Warm yellow-orange
  fill_solid(leds, LED_COUNT, warmColor);
}

void alertAnimation() {
  // Gentle wave effect to get attention without being jarring
  for (int i = 0; i < LED_COUNT; i++) {
    float wavePhase = (millis() / 500.0) + (i * 0.3);
    uint8_t brightness = (sin(wavePhase) + 1) * 80 + 50; // 50-210 range
    leds[i] = CHSV(160, 200, brightness); // Cyan-blue hue
  }
}

void testIndividualLEDs() {
  static int testLED = 0;
  static unsigned long lastLEDChange = 0;
  
  if (millis() - lastLEDChange > 200) {
    testLED = (testLED + 1) % LED_COUNT;
    lastLEDChange = millis();
  }
  
  FastLED.setBrightness(BRIGHTNESS);
  fill_solid(leds, LED_COUNT, CRGB::Black);
  leds[testLED] = CRGB::White;
  
  // Print LED position occasionally
  static int lastPrintedLED = -1;
  if (testLED % 10 == 0 && testLED != lastPrintedLED) {
    Serial.printf("Testing LED #%d/%d\n", testLED, LED_COUNT);
    lastPrintedLED = testLED;
  }
}