/*
 * Pixel Plant - PIR Motion Sensor Test
 * 
 * Tests the PIR motion sensor (BL412) functionality
 * Verifies motion detection and sensor responsiveness
 * 
 * Hardware: ESP32-S3 + PIR Sensor BL412
 * Pin: GPIO 22 (configurable)
 */

// PIR Configuration
#define PIR_PIN           22        // GPIO pin connected to PIR sensor output
#define BUILT_IN_LED      2         // Built-in LED for visual feedback
#define DEBOUNCE_TIME     200       // Minimum time between motion events (ms)
#define CALIBRATION_TIME  10000     // PIR sensor calibration time (ms)

// Motion tracking
bool motionDetected = false;
bool lastMotionState = false;
unsigned long lastMotionTime = 0;
unsigned long motionStartTime = 0;
unsigned long motionDuration = 0;
int motionCount = 0;
unsigned long sessionStartTime = 0;

// Statistics
unsigned long totalMotionTime = 0;
unsigned long longestMotionDuration = 0;
unsigned long shortestMotionDuration = ULONG_MAX;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n🌿 Pixel Plant PIR Motion Sensor Test");
  Serial.println("=====================================");
  Serial.printf("PIR Sensor Pin: GPIO %d\n", PIR_PIN);
  Serial.printf("Status LED Pin: GPIO %d\n", BUILT_IN_LED);
  Serial.printf("Debounce Time: %d ms\n", DEBOUNCE_TIME);
  Serial.println("=====================================\n");
  
  // Configure pins
  pinMode(PIR_PIN, INPUT);
  pinMode(BUILT_IN_LED, OUTPUT);
  digitalWrite(BUILT_IN_LED, LOW);
  
  Serial.println("🔧 Initializing PIR sensor...");
  Serial.printf("⏱️ Calibrating sensor for %d seconds...\n", CALIBRATION_TIME / 1000);
  Serial.println("Please avoid movement in front of the sensor during calibration.");
  
  // PIR sensor calibration period
  unsigned long calibrationStart = millis();
  while (millis() - calibrationStart < CALIBRATION_TIME) {
    // Show calibration progress
    static unsigned long lastProgress = 0;
    if (millis() - lastProgress > 1000) {
      int secondsLeft = (CALIBRATION_TIME - (millis() - calibrationStart)) / 1000;
      Serial.printf("   Calibrating... %d seconds remaining\n", secondsLeft);
      lastProgress = millis();
      
      // Blink LED during calibration
      digitalWrite(BUILT_IN_LED, !digitalRead(BUILT_IN_LED));
    }
  }
  
  digitalWrite(BUILT_IN_LED, LOW);
  Serial.println("✅ PIR sensor calibration complete!");
  Serial.println("\n📋 Test Instructions:");
  Serial.println("• Wave your hand in front of the sensor");
  Serial.println("• Walk around the sensor area");
  Serial.println("• Try different distances and speeds");
  Serial.println("• LED will light up when motion is detected");
  Serial.println("• Motion events will be logged to serial monitor");
  Serial.println("\n🎯 Starting motion detection...");
  Serial.println("=================================================\n");
  
  sessionStartTime = millis();
}

void loop() {
  readPIRSensor();
  updateStatistics();
  printPeriodicStatus();
  delay(50); // Small delay for stability
}

void readPIRSensor() {
  bool currentState = digitalRead(PIR_PIN);
  unsigned long currentTime = millis();
  
  // Debounce the sensor reading
  if (currentState != lastMotionState) {
    if (currentTime - lastMotionTime > DEBOUNCE_TIME) {
      
      if (currentState == HIGH && !motionDetected) {
        // Motion started
        motionDetected = true;
        motionStartTime = currentTime;
        motionCount++;
        
        digitalWrite(BUILT_IN_LED, HIGH);
        
        Serial.printf("🚶 Motion #%d detected at %lu ms\n", motionCount, currentTime);
        
      } else if (currentState == LOW && motionDetected) {
        // Motion ended
        motionDetected = false;
        motionDuration = currentTime - motionStartTime;
        totalMotionTime += motionDuration;
        
        digitalWrite(BUILT_IN_LED, LOW);
        
        // Update duration statistics
        if (motionDuration > longestMotionDuration) {
          longestMotionDuration = motionDuration;
        }
        if (motionDuration < shortestMotionDuration) {
          shortestMotionDuration = motionDuration;
        }
        
        Serial.printf("✋ Motion ended - Duration: %lu ms\n", motionDuration);
        
        // Classify motion type based on duration
        classifyMotion(motionDuration);
      }
      
      lastMotionTime = currentTime;
    }
  }
  
  lastMotionState = currentState;
}

void classifyMotion(unsigned long duration) {
  String motionType;
  String emoji;
  
  if (duration < 500) {
    motionType = "Quick movement";
    emoji = "⚡";
  } else if (duration < 2000) {
    motionType = "Normal movement";
    emoji = "👋";
  } else if (duration < 5000) {
    motionType = "Sustained movement";
    emoji = "🚶";
  } else {
    motionType = "Extended presence";
    emoji = "🧍";
  }
  
  Serial.printf("   %s %s (%lu ms)\n", emoji.c_str(), motionType.c_str(), duration);
}

void updateStatistics() {
  // Update any real-time statistics here if needed
  // This function is called every loop iteration
}

void printPeriodicStatus() {
  static unsigned long lastStatusPrint = 0;
  unsigned long currentTime = millis();
  
  // Print status every 30 seconds
  if (currentTime - lastStatusPrint > 30000) {
    printDetailedStatus();
    lastStatusPrint = currentTime;
  }
}

void printDetailedStatus() {
  unsigned long sessionDuration = millis() - sessionStartTime;
  float sessionMinutes = sessionDuration / 60000.0;
  
  Serial.println("\n📊 Motion Detection Statistics");
  Serial.println("================================");
  Serial.printf("Session Duration: %.1f minutes\n", sessionMinutes);
  Serial.printf("Total Motion Events: %d\n", motionCount);
  
  if (motionCount > 0) {
    Serial.printf("Total Motion Time: %.1f seconds\n", totalMotionTime / 1000.0);
    Serial.printf("Average Motion Duration: %.1f seconds\n", 
                  (totalMotionTime / motionCount) / 1000.0);
    Serial.printf("Longest Motion: %.1f seconds\n", longestMotionDuration / 1000.0);
    Serial.printf("Shortest Motion: %.1f seconds\n", shortestMotionDuration / 1000.0);
    Serial.printf("Motion Frequency: %.1f events/minute\n", motionCount / sessionMinutes);
    Serial.printf("Activity Percentage: %.1f%%\n", 
                  (totalMotionTime / (float)sessionDuration) * 100);
  }
  
  // Current sensor state
  Serial.printf("Current State: %s\n", digitalRead(PIR_PIN) ? "MOTION" : "STILL");
  
  // PIR sensor tips
  if (motionCount == 0 && sessionMinutes > 2) {
    Serial.println("\n💡 No motion detected yet. Try:");
    Serial.println("   • Check wiring connections");
    Serial.println("   • Verify 3.3V power supply");
    Serial.println("   • Move closer to the sensor");
    Serial.println("   • Check sensor sensitivity adjustment");
  } else if (motionCount > 0) {
    Serial.println("\n✅ PIR sensor is working correctly!");
  }
  
  Serial.println("================================\n");
}

// Function to test sensor responsiveness
void runSensitivityTest() {
  Serial.println("\n🧪 Running PIR Sensitivity Test");
  Serial.println("Please follow these instructions:");
  Serial.println("1. Stand still for 10 seconds");
  Serial.println("2. Wave your hand slowly");
  Serial.println("3. Wave your hand quickly");
  Serial.println("4. Walk past the sensor");
  Serial.println("5. Stand at different distances");
  
  // This could be triggered by serial command if needed
}

// Helper function to get motion rate
float getMotionRate() {
  unsigned long sessionDuration = millis() - sessionStartTime;
  if (sessionDuration < 60000) return 0; // Need at least 1 minute of data
  
  return (motionCount * 60000.0) / sessionDuration; // Events per minute
}

// Helper function to check if sensor is responsive
bool isSensorResponsive() {
  unsigned long sessionDuration = millis() - sessionStartTime;
  if (sessionDuration < 120000) return true; // Give 2 minutes before checking
  
  return motionCount > 0; // At least one motion event in 2+ minutes
}

// Function that could be called from main firmware
bool testPIRSensor() {
  Serial.println("🔍 Quick PIR sensor test...");
  
  int motionsBefore = motionCount;
  unsigned long testStart = millis();
  
  Serial.println("Wave your hand in front of the sensor now!");
  
  // Wait up to 10 seconds for motion
  while (millis() - testStart < 10000) {
    readPIRSensor();
    if (motionCount > motionsBefore) {
      Serial.println("✅ PIR sensor test PASSED");
      return true;
    }
    delay(100);
  }
  
  Serial.println("❌ PIR sensor test FAILED - no motion detected");
  return false;
}