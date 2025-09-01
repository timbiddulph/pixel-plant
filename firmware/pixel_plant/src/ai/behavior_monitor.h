/*
 * Pixel Plant Behavior Monitor
 * 
 * AI system that observes and analyzes user behavior patterns to determine
 * when caring interventions are needed. Uses computer vision, motion detection,
 * and pattern learning to understand user wellbeing needs.
 */

#ifndef BEHAVIOR_MONITOR_H
#define BEHAVIOR_MONITOR_H

#include <Arduino.h>
#include <vector>
#include "../utils/logger.h"
#include "../../config.h"

// Behavior data structure shared with personality engine
struct BehaviorData {
  // Activity metrics
  unsigned long inactivityMinutes;
  bool isUserPresent;
  bool isUserMoving;
  float activityLevel;           // 0.0-1.0 activity intensity
  
  // Posture and position
  bool isUserSitting;
  bool isUserStanding;
  float postureQuality;          // 0.0-1.0 posture assessment
  
  // Health indicators
  bool needsHydration;
  bool needsMovement;
  bool needsPostureAdjustment;
  bool needsBreak;
  bool needsSupport;             // Emotional support needed
  
  // Positive behaviors (for celebration)
  bool hasPositiveBehavior;
  bool tookBreak;
  bool improvedPosture;
  bool gotUpAndMoved;
  
  // Timing data
  unsigned long lastMovementTime;
  unsigned long lastBreakTime;
  unsigned long sessionStartTime;
  unsigned long currentSessionDuration;
  
  // Environmental context
  float lightLevel;
  float estimatedStress;         // 0.0-1.0 based on behavior patterns
  int timeOfDay;                 // Hour 0-23
};

// Activity pattern for learning user habits
struct ActivityPattern {
  int hourOfDay;
  float typicalActivity;         // Expected activity level
  float confidence;              // How confident we are in this pattern
  unsigned long samples;         // Number of observations
  bool isWorkTime;              // Whether this is typically work time
};

// User behavioral profile
struct UserProfile {
  // Activity patterns by hour
  ActivityPattern hourlyPatterns[24];
  
  // Personal preferences learned over time
  float preferredBreakInterval;  // Minutes between breaks
  float hydrationFrequency;      // Reminders per hour
  float movementSensitivity;     // How much movement is "enough"
  
  // Response patterns
  bool respondsToGentle;
  bool needsUrgentReminders;
  float effectiveReminderTiming; // Best time gaps for reminders
  
  // Health goals
  int targetStepsPerHour;
  int targetBreaksPerDay;
  float targetActivityLevel;
  
  // Learning metadata
  unsigned long profileAge;      // How long we've been learning
  float learningConfidence;      // How much we trust our patterns
};

class BehaviorMonitor {
private:
  // Current behavior state
  BehaviorData currentBehavior;
  UserProfile userProfile;
  
  // Sensor data tracking
  unsigned long lastMotionTime;
  unsigned long sessionStartTime;
  bool motionDetected;
  bool userPresent;
  
  // Computer vision data
  bool cameraAvailable;
  float lastPostureScore;
  bool faceDetected;
  unsigned long lastFaceTime;
  
  // Activity tracking
  std::vector<float> recentActivity; // Rolling activity window
  float currentActivityLevel;
  unsigned long activityWindowStart;
  
  // Pattern learning
  bool learningEnabled;
  float learningRate;
  unsigned long learningStartTime;
  
  // Reminder timing
  unsigned long lastHydrationReminder;
  unsigned long lastMovementReminder;
  unsigned long lastPostureReminder;
  
  // Sleep/wake detection
  bool sleepModeActive;
  unsigned long lastWakeTime;
  
  // Internal analysis methods
  void updateActivityLevel();
  void updatePostureAssessment();
  void updatePresenceDetection();
  void updateHealthNeeds();
  void updatePositiveBehaviors();
  void learnUserPatterns();
  bool isWorkingHours() const;
  float calculateStressLevel() const;
  
public:
  BehaviorMonitor();
  ~BehaviorMonitor();
  
  // Initialization
  bool initialize();
  
  // Main update cycle
  void update();
  BehaviorData getCurrentBehavior() const { return currentBehavior; }
  
  // Sensor input processing
  void processMotionSensor(bool motionDetected);
  void processCameraData(bool faceDetected, float postureScore);
  void processEnvironmentalData(float lightLevel);
  
  // Behavior analysis
  bool needsReminder(const BehaviorData& behavior) const;
  bool isHydrationReminderDue() const;
  bool isMovementReminderDue() const;
  bool isPostureReminderDue() const;
  bool hasUserResponded() const;
  
  // Pattern learning
  void enableLearning(bool enable = true) { learningEnabled = enable; }
  void recordUserResponse(bool positive);
  void recordHealthyBehavior(const String& behavior);
  void updateUserPattern(int hour, float activityLevel);
  
  // User profile management
  UserProfile getUserProfile() const { return userProfile; }
  void setUserProfile(const UserProfile& profile);
  float getPatternConfidence() const;
  void resetLearning();
  
  // Sleep mode management
  void setSleepMode(bool sleeping);
  bool isSleepMode() const { return sleepModeActive; }
  void wakeUp();
  
  // Activity goals and tracking
  void setActivityGoals(int stepsPerHour, int breaksPerDay);
  bool isActivityGoalMet() const;
  float getActivityGoalProgress() const;
  
  // Health reminders
  void resetHydrationTimer();
  void resetMovementTimer();
  void resetPostureTimer();
  void snoozeReminders(unsigned long minutes);
  
  // Behavior insights
  String getStatusString() const;
  String getActivitySummary() const;
  String getHealthRecommendations() const;
  
  // Time-based behavior
  void setWorkingHours(int startHour, int endHour);
  bool isInWorkingHours() const;
  float getExpectedActivityLevel() const;
  
  // Advanced features
  void detectBreakTaken();
  void detectPostureImprovement();
  void detectStressIndicators();
  bool predictUserNeed() const;
  
  // Calibration and setup
  void calibrateForUser();
  void setPersonalityAlignment(float caringLevel);
  void adjustSensitivity(float multiplier);
  
  // Data export/import for learning persistence
  void saveUserProfile();
  void loadUserProfile();
  
  // Debug and development
  void printBehaviorData() const;
  void simulateBehavior(const String& behaviorType);
  void setTestMode(bool enabled);
};

// Helper functions for behavior analysis
namespace BehaviorAnalysis {
  float calculatePostureScore(/* camera data parameters */);
  bool detectSittingPosture(/* camera data */);
  bool detectStandingPosture(/* camera data */);
  float estimateStressFromBehavior(const BehaviorData& data);
  bool isHealthyActivityLevel(float level);
  String describeBehaviorPattern(const BehaviorData& data);
}

// Constants for behavior thresholds
namespace BehaviorThresholds {
  const float MIN_HEALTHY_ACTIVITY = 0.3;
  const float MAX_SEDENTARY_TIME = 60.0; // minutes
  const float GOOD_POSTURE_THRESHOLD = 0.7;
  const float STRESS_INDICATOR_THRESHOLD = 0.6;
  const unsigned long PRESENCE_TIMEOUT = 300000; // 5 minutes
  const unsigned long BREAK_DETECTION_MIN = 120000; // 2 minutes minimum break
}

#endif // BEHAVIOR_MONITOR_H