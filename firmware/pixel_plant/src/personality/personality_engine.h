/*
 * Pixel Plant Personality Engine
 * 
 * The heart of the caring AI companion - generates personality-rich responses
 * that feel genuine, supportive, and adaptive to user behavior patterns.
 * 
 * Core Philosophy:
 * - Genuine care over algorithmic responses
 * - Gentle persistence without nagging
 * - Emotional intelligence and context awareness
 * - Growth-oriented celebration of user improvements
 */

#ifndef PERSONALITY_ENGINE_H
#define PERSONALITY_ENGINE_H

#include <Arduino.h>
#include <vector>
#include "../utils/logger.h"
#include "../../config.h"

// Forward declarations
struct BehaviorData;
struct UserContext;

// Personality response types
enum ResponseType {
  RESPONSE_GREETING = 0,
  RESPONSE_HYDRATION,
  RESPONSE_MOVEMENT,
  RESPONSE_POSTURE,
  RESPONSE_BREAK,
  RESPONSE_ENCOURAGEMENT,
  RESPONSE_CELEBRATION,
  RESPONSE_CONCERN,
  RESPONSE_URGENT,
  RESPONSE_GOODNIGHT,
  RESPONSE_COUNT
};

// Care escalation levels
enum CareLevel {
  CARE_GENTLE = 0,      // Soft suggestions
  CARE_ENCOURAGING,     // Friendly reminders
  CARE_CONCERNED,       // More persistent care
  CARE_WORRIED,         // Urgent attention needed
  CARE_COUNT
};

// Message structure for varied responses
struct PersonalityMessage {
  String text;
  MoodType mood;
  CareLevel careLevel;
  unsigned long timestamp;
  int useCount;           // Track how often used to ensure variety
};

// User interaction history
struct InteractionHistory {
  ResponseType lastResponseType;
  unsigned long lastResponseTime;
  bool userResponded;
  int consecutiveIgnored;
  float responseEffectiveness; // 0.0-1.0 based on user response
};

class PersonalityEngine {
private:
  // Core personality state
  MoodType currentMood;
  CareLevel currentCareLevel;
  float caringIntensity;      // 0.0-1.0 how much care to show
  float personalityWarmth;    // 0.0-1.0 how warm/friendly to be
  
  // Message management
  std::vector<PersonalityMessage> messageBank[RESPONSE_COUNT];
  std::vector<String> messageQueue;
  unsigned long lastMessageTime;
  
  // User adaptation
  InteractionHistory history;
  String userName;
  float userPreferences[RESPONSE_COUNT]; // What response styles work best
  
  // Learning system
  bool learningEnabled;
  float adaptationRate;
  unsigned long learningStartTime;
  
  // Response timing
  unsigned long responseCooldown;
  bool canRespond;
  
  // Internal methods
  void initializeMessageBank();
  void loadHydrationMessages();
  void loadMovementMessages();
  void loadPostureMessages();
  void loadEncouragementMessages();
  void loadCelebrationMessages();
  void loadConcernMessages();
  void loadGreetingMessages();
  
  PersonalityMessage* selectBestMessage(ResponseType type);
  void updateMessageEffectiveness(PersonalityMessage* message, bool wasEffective);
  String personalizeMessage(const String& baseMessage);
  void escalateCareLevel();
  void reduceCareLevel();
  
public:
  PersonalityEngine();
  ~PersonalityEngine();
  
  // Initialization
  bool initialize();
  void setUserName(const String& name);
  void setPersonalityTraits(float warmth, float caringIntensity);
  
  // Core personality functions
  MoodType getCurrentMood() const { return currentMood; }
  String getMoodString() const;
  void setMood(MoodType mood);
  void updateMood(const BehaviorData& behavior);
  
  // Message generation
  String generateCaringResponse();
  String generateCaringResponse(ResponseType type);
  String generateUrgentResponse();
  String generateCelebrationMessage(const String& achievement);
  String generateContextualResponse(const BehaviorData& behavior);
  
  // Message queue management
  void queueMessage(const String& message);
  void queueMessage(ResponseType type);
  bool hasQueuedMessage() const { return !messageQueue.empty(); }
  String getNextMessage();
  void clearMessageQueue();
  
  // User interaction tracking
  void recordUserResponse(ResponseType responseType, bool effective);
  void recordUserIgnored(ResponseType responseType);
  void processObservation(const BehaviorData& behavior);
  
  // Learning and adaptation
  void enableLearning(bool enable = true) { learningEnabled = enable; }
  void setAdaptationRate(float rate) { adaptationRate = rate; }
  void adaptToUser(ResponseType type, float effectiveness);
  void resetLearning();
  
  // Personality customization
  void setCareLevel(CareLevel level);
  CareLevel getCurrentCareLevel() const { return currentCareLevel; }
  void adjustCaringIntensity(float delta);
  
  // Response control
  bool canRespondNow() const;
  void setResponseCooldown(unsigned long cooldownMs);
  void enableResponses(bool enable = true) { canRespond = enable; }
  
  // Personality insights
  String getPersonalityStatus() const;
  float getResponseEffectiveness(ResponseType type) const;
  int getConsecutiveIgnoredCount() const { return history.consecutiveIgnored; }
  
  // Special behaviors
  String generateWakeupMessage();
  String generateGoodNightMessage();
  String generateFirstTimeGreeting();
  String generateReturningUserGreeting();
  
  // Mood-specific responses
  String generateHappyResponse();
  String generateConcernedResponse();
  String generateWorriedResponse();
  String generateCalmingResponse();
  
  // Context awareness
  void setTimeOfDay(int hour);
  void setUserWorkingState(bool isWorking);
  void setEnvironmentalContext(float lightLevel, float noiseLevel);
  
  // Persistence
  void savePersonalityState();
  void loadPersonalityState();
  
  // Debug and development
  void printPersonalityState() const;
  void simulateUserInteraction(ResponseType type, bool positive);
};

// Helper functions for personality traits
namespace PersonalityTraits {
  String getCaringPhrase(CareLevel level);
  String getEncouragementPhrase();
  String getGentleReminderPhrase();
  String getCelebrationPhrase();
  MoodType behaviorToMood(const BehaviorData& behavior);
  float calculateCaringUrgency(const BehaviorData& behavior);
}

// User context structure for advanced personalization
struct UserContext {
  String name;
  int workStartHour;
  int workEndHour;
  int preferredBreakInterval;
  float caringPreference;     // How much care the user wants
  bool likesEncouragement;
  bool respondsToGentle;
  bool needsUrgentReminders;
  unsigned long totalInteractionTime;
  int successfulHealthyBehaviors;
};

#endif // PERSONALITY_ENGINE_H