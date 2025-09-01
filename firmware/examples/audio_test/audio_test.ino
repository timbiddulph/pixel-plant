/*
 * Pixel Plant - Audio System Test
 * 
 * Tests the I2S audio amplifier (MAX98357A) and speaker
 * Verifies audio output and basic sound generation
 * 
 * Hardware: ESP32-S3 + MAX98357A + Speaker
 * Pins: GPIO 19 (BCLK), GPIO 20 (LRC), GPIO 21 (DIN)
 */

#include "driver/i2s.h"
#include <math.h>

// I2S Configuration
#define I2S_PORT          I2S_NUM_0
#define I2S_SAMPLE_RATE   22050
#define I2S_BCLK_PIN      19        // Bit clock
#define I2S_LRC_PIN       20        // Left/Right clock  
#define I2S_DIN_PIN       21        // Data input
#define I2S_BITS          16        // Bits per sample
#define I2S_CHANNELS      1         // Mono

// Audio generation
#define BUFFER_SIZE       512
#define PI                3.14159265359

// Test parameters
int16_t audioBuffer[BUFFER_SIZE];
int currentTest = 0;
unsigned long lastTestChange = 0;
unsigned long testDuration = 8000; // Each test runs for 8 seconds

// Audio state
float phase = 0;
float frequency = 440; // A note
float amplitude = 0.3; // Volume level (0.0 - 1.0)

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n🌿 Pixel Plant Audio Test Starting...");
  Serial.println("======================================");
  Serial.printf("Sample Rate: %d Hz\n", I2S_SAMPLE_RATE);
  Serial.printf("Channels: %d (Mono)\n", I2S_CHANNELS);
  Serial.printf("Bits per Sample: %d\n", I2S_BITS);
  Serial.printf("BCLK Pin: GPIO %d\n", I2S_BCLK_PIN);
  Serial.printf("LRC Pin: GPIO %d\n", I2S_LRC_PIN);
  Serial.printf("DIN Pin: GPIO %d\n", I2S_DIN_PIN);
  Serial.println("======================================\n");
  
  // Initialize I2S
  if (initializeI2S()) {
    Serial.println("✅ I2S Audio initialized successfully!");
  } else {
    Serial.println("❌ I2S Audio initialization failed!");
    return;
  }
  
  Serial.println("\nStarting audio tests...");
  Serial.println("Each test runs for 8 seconds");
  Serial.println("Tests will cycle automatically");
  Serial.println("======================================\n");
  Serial.println("🔊 Make sure your speaker volume is at a comfortable level!");
  Serial.println("If you don't hear anything, check your wiring and power.\n");
  
  lastTestChange = millis();
}

void loop() {
  // Check if it's time to switch tests
  if (millis() - lastTestChange > testDuration) {
    currentTest = (currentTest + 1) % 7; // 7 different tests
    lastTestChange = millis();
    printCurrentTest();
    
    // Reset phase for clean test transitions
    phase = 0;
    delay(500); // Brief pause between tests
  }
  
  // Generate audio based on current test
  switch (currentTest) {
    case 0:
      testSilence();
      break;
    case 1:
      testSineWave(440); // A4 note
      break;
    case 2:
      testSineWave(880); // A5 note (octave higher)
      break;
    case 3:
      testFrequencySweep();
      break;
    case 4:
      testBeeps();
      break;
    case 5:
      testCaringTones();
      break;
    case 6:
      testWhiteNoise();
      break;
  }
  
  // Send audio buffer to I2S
  size_t bytesWritten;
  i2s_write(I2S_PORT, audioBuffer, BUFFER_SIZE * sizeof(int16_t), &bytesWritten, portMAX_DELAY);
}

bool initializeI2S() {
  // I2S configuration
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
    .sample_rate = I2S_SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT, // Mono - use left channel
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = BUFFER_SIZE,
    .use_apll = false,
    .tx_desc_auto_clear = true
  };
  
  // I2S pin configuration
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_BCLK_PIN,
    .ws_io_num = I2S_LRC_PIN,
    .data_out_num = I2S_DIN_PIN,
    .data_in_num = I2S_PIN_NO_CHANGE
  };
  
  // Install and start I2S driver
  esp_err_t result = i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  if (result != ESP_OK) {
    Serial.printf("❌ I2S driver install failed: %d\n", result);
    return false;
  }
  
  result = i2s_set_pin(I2S_PORT, &pin_config);
  if (result != ESP_OK) {
    Serial.printf("❌ I2S pin setup failed: %d\n", result);
    return false;
  }
  
  result = i2s_start(I2S_PORT);
  if (result != ESP_OK) {
    Serial.printf("❌ I2S start failed: %d\n", result);
    return false;
  }
  
  return true;
}

void printCurrentTest() {
  Serial.print("🔊 Test ");
  Serial.print(currentTest + 1);
  Serial.print("/7: ");
  
  switch (currentTest) {
    case 0: Serial.println("Silence (should be quiet)"); break;
    case 1: Serial.println("Pure Sine Wave 440Hz (A4 note)"); break;
    case 2: Serial.println("Pure Sine Wave 880Hz (A5 note)"); break;
    case 3: Serial.println("Frequency Sweep (200Hz to 2000Hz)"); break;
    case 4: Serial.println("Notification Beeps"); break;
    case 5: Serial.println("Caring Tones (what Pixel Plant might sound like)"); break;
    case 6: Serial.println("White Noise (audio connection test)"); break;
  }
}

void testSilence() {
  // Fill buffer with silence
  for (int i = 0; i < BUFFER_SIZE; i++) {
    audioBuffer[i] = 0;
  }
}

void testSineWave(float freq) {
  frequency = freq;
  amplitude = 0.3; // Moderate volume
  
  for (int i = 0; i < BUFFER_SIZE; i++) {
    float sample = sin(phase) * amplitude;
    audioBuffer[i] = (int16_t)(sample * 32767); // Convert to 16-bit signed
    
    phase += 2.0 * PI * frequency / I2S_SAMPLE_RATE;
    if (phase > 2.0 * PI) {
      phase -= 2.0 * PI;
    }
  }
}

void testFrequencySweep() {
  static float sweepStartTime = 0;
  if (sweepStartTime == 0) {
    sweepStartTime = millis();
  }
  
  // Sweep from 200Hz to 2000Hz over 8 seconds
  float sweepProgress = (millis() - sweepStartTime) / (float)testDuration;
  if (sweepProgress > 1.0) sweepProgress = 1.0;
  
  frequency = 200 + (2000 - 200) * sweepProgress;
  amplitude = 0.25;
  
  for (int i = 0; i < BUFFER_SIZE; i++) {
    float sample = sin(phase) * amplitude;
    audioBuffer[i] = (int16_t)(sample * 32767);
    
    phase += 2.0 * PI * frequency / I2S_SAMPLE_RATE;
    if (phase > 2.0 * PI) {
      phase -= 2.0 * PI;
    }
  }
  
  // Reset sweep at end of test cycle
  if (currentTest != 3) {
    sweepStartTime = 0;
  }
}

void testBeeps() {
  static unsigned long beepStartTime = 0;
  static bool inBeep = false;
  static int beepCount = 0;
  
  unsigned long currentTime = millis();
  
  if (beepStartTime == 0) {
    beepStartTime = currentTime;
    inBeep = true;
    beepCount = 0;
  }
  
  // Beep pattern: 200ms on, 300ms off, repeat
  unsigned long timeSinceStart = currentTime - beepStartTime;
  unsigned long cycleTime = timeSinceStart % 500; // 500ms cycle
  
  if (cycleTime < 200) {
    // Beep on
    if (!inBeep) {
      inBeep = true;
      beepCount++;
      Serial.printf("  Beep #%d\n", beepCount);
    }
    testSineWave(800); // Higher pitched beep
  } else {
    // Beep off
    inBeep = false;
    testSilence();
  }
  
  // Reset at end of test cycle
  if (currentTest != 4) {
    beepStartTime = 0;
  }
}

void testCaringTones() {
  // Generate soothing, caring tones like what the Pixel Plant might use
  static float carePhase1 = 0;
  static float carePhase2 = 0;
  static unsigned long careStartTime = 0;
  
  if (careStartTime == 0) {
    careStartTime = millis();
  }
  
  // Two harmonious sine waves with gentle amplitude modulation
  float time = (millis() - careStartTime) / 1000.0;
  float modulation = (sin(time * 0.5) + 1) * 0.5; // Slow amplitude modulation
  
  amplitude = 0.15 * modulation; // Gentle, varying volume
  
  for (int i = 0; i < BUFFER_SIZE; i++) {
    // Two gentle frequencies creating harmony
    float sample1 = sin(carePhase1) * amplitude;
    float sample2 = sin(carePhase2) * amplitude * 0.5; // Quieter harmonic
    
    float combinedSample = (sample1 + sample2) * 0.7; // Mix and reduce volume
    audioBuffer[i] = (int16_t)(combinedSample * 32767);
    
    // Primary tone around 523Hz (C5)
    carePhase1 += 2.0 * PI * 523 / I2S_SAMPLE_RATE;
    if (carePhase1 > 2.0 * PI) carePhase1 -= 2.0 * PI;
    
    // Harmonic at 659Hz (E5) - creates a gentle major third
    carePhase2 += 2.0 * PI * 659 / I2S_SAMPLE_RATE;
    if (carePhase2 > 2.0 * PI) carePhase2 -= 2.0 * PI;
  }
  
  // Reset at end of test cycle
  if (currentTest != 5) {
    careStartTime = 0;
    carePhase1 = 0;
    carePhase2 = 0;
  }
}

void testWhiteNoise() {
  // Generate white noise to test audio connection
  amplitude = 0.1; // Keep noise quiet
  
  for (int i = 0; i < BUFFER_SIZE; i++) {
    float sample = ((float)random(-1000, 1000) / 1000.0) * amplitude;
    audioBuffer[i] = (int16_t)(sample * 32767);
  }
}

// Utility function for future use
void playTone(float freq, float vol, int durationMs) {
  unsigned long startTime = millis();
  float tonePhase = 0;
  
  while (millis() - startTime < durationMs) {
    for (int i = 0; i < BUFFER_SIZE; i++) {
      float sample = sin(tonePhase) * vol;
      audioBuffer[i] = (int16_t)(sample * 32767);
      
      tonePhase += 2.0 * PI * freq / I2S_SAMPLE_RATE;
      if (tonePhase > 2.0 * PI) {
        tonePhase -= 2.0 * PI;
      }
    }
    
    size_t bytesWritten;
    i2s_write(I2S_PORT, audioBuffer, BUFFER_SIZE * sizeof(int16_t), &bytesWritten, portMAX_DELAY);
  }
}