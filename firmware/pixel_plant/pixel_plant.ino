/*
 * Pixel Plant AI Companion
 * Main Arduino Sketch for ESP32-S3
 * 
 * A caring AI desktop companion inspired by Becky Chambers' novel
 * "The Long Way to a Small, Angry Planet"
 * 
 * Hardware: DFRobot FireBeetle 2 ESP32-S3 with Camera
 * 
 * Author: Pixel Plant Community
 * License: MIT
 */

#include "config.h"
#include "src/hardware/hardware_manager.h"
#include "src/personality/personality_engine.h"
#include "src/ai/behavior_monitor.h"
#include "src/utils/logger.h"

// Global component managers
HardwareManager hardware;
PersonalityEngine personality;
BehaviorMonitor behaviorAI;
Logger logger;

// System state
SystemState currentState = SYSTEM_INITIALIZING;
unsigned long lastUpdateTime = 0;
unsigned long lastHeartbeat = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(SERIAL_BAUD_RATE);
  delay(1000);
  
  logger.info("🌿 Pixel Plant starting up...");
  logger.info("Firmware version: " + String(FIRMWARE_VERSION));
  logger.info("Hardware: ESP32-S3 FireBeetle");
  
  // Initialize hardware components
  if (!hardware.initialize()) {
    logger.error("❌ Hardware initialization failed!");
    currentState = SYSTEM_ERROR;
    return;
  }
  
  // Initialize AI systems
  if (!behaviorAI.initialize()) {
    logger.warning("⚠️ AI systems not available - running in basic mode");
  }
  
  // Initialize personality engine
  personality.initialize();
  personality.setMood(MOOD_HAPPY);
  
  // Show startup animation
  hardware.leds.showStartupAnimation();
  hardware.audio.playStartupSound();
  
  logger.info("✅ Pixel Plant ready to care for you!");
  currentState = SYSTEM_READY;
}

void loop() {
  unsigned long currentTime = millis();
  
  // System heartbeat
  if (currentTime - lastHeartbeat > HEARTBEAT_INTERVAL) {
    systemHeartbeat();
    lastHeartbeat = currentTime;
  }
  
  // Main update cycle
  if (currentTime - lastUpdateTime > UPDATE_INTERVAL) {
    mainUpdate();
    lastUpdateTime = currentTime;
  }
  
  // Handle any immediate tasks
  handleImmediateTasks();
  
  // Small delay to prevent watchdog issues
  delay(10);
}

void mainUpdate() {
  switch (currentState) {
    case SYSTEM_READY:
      runNormalOperation();
      break;
      
    case SYSTEM_CARING:
      runCaringMode();
      break;
      
    case SYSTEM_CONCERNED:
      runConcernedMode();
      break;
      
    case SYSTEM_SLEEPING:
      runSleepMode();
      break;
      
    case SYSTEM_ERROR:
      runErrorRecovery();
      break;
      
    default:
      logger.error("Unknown system state: " + String(currentState));
      currentState = SYSTEM_ERROR;
  }
}

void runNormalOperation() {
  // Monitor user behavior
  BehaviorData behavior = behaviorAI.getCurrentBehavior();
  
  // Update personality based on observations
  personality.processObservation(behavior);
  
  // Check if we need to provide care
  if (behaviorAI.needsReminder(behavior)) {
    transitionToCaring(behavior);
  }
  
  // Update visual display
  hardware.leds.updateMoodDisplay(personality.getCurrentMood());
  
  // Handle any scheduled reminders
  checkScheduledReminders();
}

void runCaringMode() {
  // Generate caring response
  String response = personality.generateCaringResponse();
  
  // Display caring animation
  hardware.leds.showCaringAnimation();
  
  // Speak caring message
  hardware.audio.speakMessage(response);
  
  logger.info("💚 Caring message: " + response);
  
  // Return to normal operation
  currentState = SYSTEM_READY;
}

void runConcernedMode() {
  // More persistent caring behavior
  MoodType currentMood = personality.getCurrentMood();
  
  if (currentMood == MOOD_WORRIED) {
    // Show more urgent animation
    hardware.leds.showConcernedAnimation();
    
    // Speak with more concern
    String urgentResponse = personality.generateUrgentResponse();
    hardware.audio.speakMessage(urgentResponse);
  }
  
  // Check if user has responded to our care
  if (behaviorAI.hasUserResponded()) {
    personality.setMood(MOOD_HAPPY);
    currentState = SYSTEM_READY;
  }
}

void runSleepMode() {
  // Gentle breathing LED pattern
  hardware.leds.showSleepingAnimation();
  
  // Reduced monitoring frequency
  behaviorAI.setSleepMode(true);
  
  // Wake up if movement detected
  if (hardware.pir.motionDetected()) {
    wakeFromSleep();
  }
}

void runErrorRecovery() {
  // Attempt to recover from errors
  hardware.leds.showErrorPattern();
  
  // Try to reinitialize failed systems
  if (millis() % 30000 == 0) { // Every 30 seconds
    logger.info("Attempting system recovery...");
    if (hardware.reinitialize()) {
      logger.info("✅ Recovery successful!");
      currentState = SYSTEM_READY;
    }
  }
}

void transitionToCaring(BehaviorData behavior) {
  logger.info("Transitioning to caring mode");
  
  // Determine appropriate level of care
  if (behavior.inactivityMinutes > URGENT_INACTIVITY_THRESHOLD) {
    personality.setMood(MOOD_WORRIED);
    currentState = SYSTEM_CONCERNED;
  } else {
    personality.setMood(MOOD_CARING);
    currentState = SYSTEM_CARING;
  }
}

void wakeFromSleep() {
  logger.info("☀️ Good morning! Pixel Plant is waking up");
  
  behaviorAI.setSleepMode(false);
  personality.setMood(MOOD_HAPPY);
  hardware.leds.showWakeupAnimation();
  hardware.audio.playWakeupSound();
  
  currentState = SYSTEM_READY;
}

void systemHeartbeat() {
  // System health monitoring
  float temperature = hardware.getSystemTemperature();
  int freeMemory = ESP.getFreeHeap();
  
  // Log system stats periodically
  static int heartbeatCount = 0;
  if (++heartbeatCount % 60 == 0) { // Every 10 minutes at 10s intervals
    logger.info("💓 Heartbeat: Temp=" + String(temperature) + "°C, Memory=" + String(freeMemory) + "B");
  }
  
  // Check for system issues
  if (temperature > MAX_OPERATING_TEMP) {
    logger.warning("🌡️ High temperature detected: " + String(temperature) + "°C");
    personality.setMood(MOOD_CONCERNED);
  }
  
  if (freeMemory < MIN_FREE_MEMORY) {
    logger.warning("💾 Low memory warning: " + String(freeMemory) + "B");
  }
}

void checkScheduledReminders() {
  // Check if it's time for scheduled health reminders
  static unsigned long lastReminderCheck = 0;
  
  if (millis() - lastReminderCheck > REMINDER_CHECK_INTERVAL) {
    // Hydration reminder
    if (behaviorAI.isHydrationReminderDue()) {
      personality.queueMessage("Hey there! You need to hydrate! 💧");
    }
    
    // Movement reminder
    if (behaviorAI.isMovementReminderDue()) {
      personality.queueMessage("How about a stretch? Take a walk! 🚶‍♀️");
    }
    
    // Posture reminder
    if (behaviorAI.isPostureReminderDue()) {
      personality.queueMessage("Time to adjust that posture! Stretch it out! 🧘");
    }
    
    lastReminderCheck = millis();
  }
}

void handleImmediateTasks() {
  // Handle any queued personality messages
  if (personality.hasQueuedMessage()) {
    String message = personality.getNextMessage();
    hardware.audio.speakMessage(message);
    hardware.leds.showMessageAnimation();
  }
  
  // Handle any urgent system tasks
  hardware.processImmediateTasks();
  
  // Handle serial commands for debugging
  handleSerialCommands();
}

void handleSerialCommands() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command == "status") {
      printSystemStatus();
    } else if (command == "test") {
      runSystemTest();
    } else if (command == "sleep") {
      currentState = SYSTEM_SLEEPING;
    } else if (command == "wake") {
      wakeFromSleep();
    } else if (command.startsWith("say ")) {
      String message = command.substring(4);
      hardware.audio.speakMessage(message);
    } else {
      logger.info("Unknown command: " + command);
    }
  }
}

void printSystemStatus() {
  Serial.println("\n=== 🌿 Pixel Plant System Status ===");
  Serial.println("State: " + String(currentState));
  Serial.println("Uptime: " + String(millis() / 1000) + "s");
  Serial.println("Free Memory: " + String(ESP.getFreeHeap()) + "B");
  Serial.println("Temperature: " + String(hardware.getSystemTemperature()) + "°C");
  Serial.println("Current Mood: " + personality.getMoodString());
  Serial.println("Behavior Status: " + behaviorAI.getStatusString());
  Serial.println("===================================\n");
}

void runSystemTest() {
  logger.info("🧪 Running system test...");
  
  // Test LEDs
  hardware.leds.runTestPattern();
  delay(2000);
  
  // Test audio
  hardware.audio.playTestTone();
  delay(1000);
  
  // Test sensors
  bool pirWorking = hardware.pir.testSensor();
  bool cameraWorking = hardware.camera.testCapture();
  
  Serial.println("LED Test: ✅");
  Serial.println("Audio Test: ✅");
  Serial.println("PIR Test: " + String(pirWorking ? "✅" : "❌"));
  Serial.println("Camera Test: " + String(cameraWorking ? "✅" : "❌"));
  
  logger.info("System test complete!");
}