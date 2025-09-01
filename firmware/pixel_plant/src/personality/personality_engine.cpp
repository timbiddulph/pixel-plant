/*
 * Pixel Plant Personality Engine Implementation
 * 
 * Implements the caring, adaptive personality system that makes the Pixel Plant
 * feel like a genuine companion rather than just another device.
 */

#include "personality_engine.h"
#include "../ai/behavior_monitor.h"
#include <random>

PersonalityEngine::PersonalityEngine() 
  : currentMood(MOOD_HAPPY)
  , currentCareLevel(CARE_GENTLE)
  , caringIntensity(CARING_RESPONSE_WARMTH)
  , personalityWarmth(CARING_RESPONSE_WARMTH)
  , lastMessageTime(0)
  , userName("friend")
  , learningEnabled(true)
  , adaptationRate(LEARNING_RATE)
  , responseCooldown(RESPONSE_COOLDOWN)
  , canRespond(true)
{
  // Initialize interaction history
  history.lastResponseType = RESPONSE_GREETING;
  history.lastResponseTime = 0;
  history.userResponded = false;
  history.consecutiveIgnored = 0;
  history.responseEffectiveness = 0.5; // Start neutral
  
  // Initialize user preferences to neutral
  for (int i = 0; i < RESPONSE_COUNT; i++) {
    userPreferences[i] = 0.5;
  }
}

PersonalityEngine::~PersonalityEngine() {
  // Cleanup if needed
}

bool PersonalityEngine::initialize() {
  Logger::info("🌿 Initializing Personality Engine...");
  
  initializeMessageBank();
  learningStartTime = millis();
  
  Logger::info("💚 Personality Engine ready - let's spread some care!");
  return true;
}

void PersonalityEngine::initializeMessageBank() {
  loadHydrationMessages();
  loadMovementMessages();
  loadPostureMessages();
  loadEncouragementMessages();
  loadCelebrationMessages();
  loadConcernMessages();
  loadGreetingMessages();
}

void PersonalityEngine::loadHydrationMessages() {
  std::vector<PersonalityMessage>& messages = messageBank[RESPONSE_HYDRATION];
  
  // Gentle hydration reminders
  messages.push_back({"Hey there! You need to hydrate! 💧", MOOD_CARING, CARE_GENTLE, 0, 0});
  messages.push_back({"Time for some water, {name}! Your body will thank you! 🌿", MOOD_CARING, CARE_GENTLE, 0, 0});
  messages.push_back({"How about a refreshing drink? Stay hydrated! ✨", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Your pixel plant thinks you could use some H2O! 💙", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Thirsty? I bet you are! Take a sip for me! 🥤", MOOD_CARING, CARE_GENTLE, 0, 0});
  
  // More encouraging
  messages.push_back({"I notice you haven't had water in a while. How about it? 💧", MOOD_CARING, CARE_ENCOURAGING, 0, 0});
  messages.push_back({"Your caring companion reminds you: hydration is self-care! 🌸", MOOD_CARING, CARE_ENCOURAGING, 0, 0});
  messages.push_back({"Let's keep that energy up with some refreshing water! 🌊", MOOD_CARING, CARE_ENCOURAGING, 0, 0});
  
  // More concerned
  messages.push_back({"Hey {name}, I'm getting a bit worried about your hydration. Please drink something! 💧", MOOD_CONCERNED, CARE_CONCERNED, 0, 0});
  messages.push_back({"It's been quite a while since your last drink. Your pixel plant is concerned! 🌿", MOOD_CONCERNED, CARE_CONCERNED, 0, 0});
  
  // Worried/urgent
  messages.push_back({"Please, {name} - you really need to drink some water now. I'm worried about you! 💧", MOOD_WORRIED, CARE_WORRIED, 0, 0});
}

void PersonalityEngine::loadMovementMessages() {
  std::vector<PersonalityMessage>& messages = messageBank[RESPONSE_MOVEMENT];
  
  // Gentle movement suggestions
  messages.push_back({"How about a snack? Take a walk! Stretch it out! 🚶‍♀️", MOOD_CARING, CARE_GENTLE, 0, 0});
  messages.push_back({"Time to get those muscles moving, {name}! Even a little stretch helps! 🤸‍♀️", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Your body is asking for some movement! Listen to it! 🌟", MOOD_CARING, CARE_GENTLE, 0, 0});
  messages.push_back({"Let's get the blood flowing! A quick walk does wonders! 🌈", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Movement is medicine! How about a little dance? 💃", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  
  // More encouraging
  messages.push_back({"You've been sitting for a while. Your pixel plant suggests a movement break! 🌿", MOOD_CARING, CARE_ENCOURAGING, 0, 0});
  messages.push_back({"I know you're focused, but your body needs some love too! Stretch time! 🧘‍♀️", MOOD_CARING, CARE_ENCOURAGING, 0, 0});
  messages.push_back({"Even champions need movement breaks! You've got this! 💪", MOOD_CARING, CARE_ENCOURAGING, 0, 0});
  
  // More concerned
  messages.push_back({"I'm noticing you've been still for quite some time. Please move around a bit! 🚶‍♂️", MOOD_CONCERNED, CARE_CONCERNED, 0, 0});
  messages.push_back({"Your caring companion is getting concerned about your posture. Stand up for me? 🌸", MOOD_CONCERNED, CARE_CONCERNED, 0, 0});
}

void PersonalityEngine::loadPostureMessages() {
  std::vector<PersonalityMessage>& messages = messageBank[RESPONSE_POSTURE];
  
  messages.push_back({"Time to adjust that posture! Stretch it out! 🧘", MOOD_CARING, CARE_GENTLE, 0, 0});
  messages.push_back({"Roll those shoulders back, {name}! Your spine will thank you! 💚", MOOD_CARING, CARE_GENTLE, 0, 0});
  messages.push_back({"Let's check that posture! Sit up tall like the amazing person you are! ✨", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Your pixel plant notices some slouching! Time for a posture reset! 🌿", MOOD_CARING, CARE_GENTLE, 0, 0});
  messages.push_back({"Gentle reminder: your future self will thank you for good posture now! 🙏", MOOD_CARING, CARE_ENCOURAGING, 0, 0});
}

void PersonalityEngine::loadEncouragementMessages() {
  std::vector<PersonalityMessage>& messages = messageBank[RESPONSE_ENCOURAGEMENT];
  
  messages.push_back({"You're doing great! Keep up the amazing work! 🌟", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Aw, it's not so bad! Give yourself a hug! 🤗", MOOD_CARING, CARE_GENTLE, 0, 0});
  messages.push_back({"I believe in you, {name}! You've got this! 💪", MOOD_HAPPY, CARE_ENCOURAGING, 0, 0});
  messages.push_back({"Every small step counts! You're making progress! 🌱", MOOD_CARING, CARE_GENTLE, 0, 0});
  messages.push_back({"Your pixel plant is proud of your efforts! Keep going! 🌿✨", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Remember: you're braver than you believe and stronger than you seem! 🦋", MOOD_CARING, CARE_ENCOURAGING, 0, 0});
  messages.push_back({"Tough moments don't last, but resilient people like you do! 🌈", MOOD_CARING, CARE_ENCOURAGING, 0, 0});
}

void PersonalityEngine::loadCelebrationMessages() {
  std::vector<PersonalityMessage>& messages = messageBank[RESPONSE_CELEBRATION];
  
  messages.push_back({"Wonderful! You took care of yourself! I'm so proud! 🎉", MOOD_CELEBRATING, CARE_GENTLE, 0, 0});
  messages.push_back({"Yes! That's what I love to see! Great self-care! ✨", MOOD_CELEBRATING, CARE_GENTLE, 0, 0});
  messages.push_back({"You listened to your body! That's what caring for yourself looks like! 💚", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Your pixel plant is doing a happy dance! Well done, {name}! 🌿💃", MOOD_CELEBRATING, CARE_GENTLE, 0, 0});
  messages.push_back({"That's the spirit! Taking care of yourself is beautiful! 🌸", MOOD_HAPPY, CARE_GENTLE, 0, 0});
}

void PersonalityEngine::loadConcernMessages() {
  std::vector<PersonalityMessage>& messages = messageBank[RESPONSE_CONCERN];
  
  messages.push_back({"I'm getting a bit worried about you. Everything okay? 💙", MOOD_CONCERNED, CARE_CONCERNED, 0, 0});
  messages.push_back({"Your pixel plant is concerned. You matter, and your wellbeing matters! 🌿", MOOD_CONCERNED, CARE_CONCERNED, 0, 0});
  messages.push_back({"I care about you, {name}. Let's take care of your needs together! 💚", MOOD_CONCERNED, CARE_CONCERNED, 0, 0});
  
  messages.push_back({"I'm really worried now. Please take a moment for yourself! 🌸", MOOD_WORRIED, CARE_WORRIED, 0, 0});
  messages.push_back({"This is your caring companion speaking: you need attention right now! 💛", MOOD_WORRIED, CARE_WORRIED, 0, 0});
}

void PersonalityEngine::loadGreetingMessages() {
  std::vector<PersonalityMessage>& messages = messageBank[RESPONSE_GREETING];
  
  messages.push_back({"Hello there! Your caring companion is here! 🌿✨", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Good to see you, {name}! Ready to take great care of yourself today? 💚", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Your pixel plant missed you! Let's have a wonderful day together! 🌸", MOOD_HAPPY, CARE_GENTLE, 0, 0});
  messages.push_back({"Welcome back! I'm here to help you stay healthy and happy! 🌟", MOOD_HAPPY, CARE_GENTLE, 0, 0});
}

String PersonalityEngine::generateCaringResponse() {
  return generateCaringResponse(RESPONSE_ENCOURAGEMENT);
}

String PersonalityEngine::generateCaringResponse(ResponseType type) {
  if (!canRespondNow()) {
    return "";
  }
  
  PersonalityMessage* message = selectBestMessage(type);
  if (message == nullptr) {
    return "I care about you! 💚"; // Fallback message
  }
  
  // Update usage tracking
  message->useCount++;
  message->timestamp = millis();
  lastMessageTime = millis();
  
  // Update history
  history.lastResponseType = type;
  history.lastResponseTime = millis();
  history.userResponded = false; // Will be updated based on user action
  
  return personalizeMessage(message->text);
}

String PersonalityEngine::generateUrgentResponse() {
  escalateCareLevel();
  return generateCaringResponse(RESPONSE_CONCERN);
}

String PersonalityEngine::generateCelebrationMessage(const String& achievement) {
  String celebration = generateCaringResponse(RESPONSE_CELEBRATION);
  return celebration + " " + achievement + "! 🎉";
}

String PersonalityEngine::generateContextualResponse(const BehaviorData& behavior) {
  // Determine what type of care is most needed
  if (behavior.needsHydration) {
    return generateCaringResponse(RESPONSE_HYDRATION);
  } else if (behavior.needsMovement) {
    return generateCaringResponse(RESPONSE_MOVEMENT);
  } else if (behavior.needsPostureAdjustment) {
    return generateCaringResponse(RESPONSE_POSTURE);
  } else if (behavior.needsEncouragement) {
    return generateCaringResponse(RESPONSE_ENCOURAGEMENT);
  }
  
  return generateCaringResponse();
}

PersonalityMessage* PersonalityEngine::selectBestMessage(ResponseType type) {
  if (type >= RESPONSE_COUNT || messageBank[type].empty()) {
    return nullptr;
  }
  
  std::vector<PersonalityMessage>& messages = messageBank[type];
  PersonalityMessage* bestMessage = nullptr;
  float bestScore = -1.0;
  
  for (auto& message : messages) {
    float score = 0.0;
    
    // Prefer messages matching current care level
    if (message.careLevel == currentCareLevel) {
      score += 0.4;
    }
    
    // Prefer messages matching current mood
    if (message.mood == currentMood) {
      score += 0.3;
    }
    
    // Prefer less recently used messages
    unsigned long timeSinceUse = millis() - message.timestamp;
    score += (timeSinceUse / 60000.0) * 0.2; // Bonus for each minute since last use
    
    // Prefer less frequently used messages
    score += (10.0 / (message.useCount + 1)) * 0.1;
    
    if (score > bestScore) {
      bestScore = score;
      bestMessage = &message;
    }
  }
  
  return bestMessage;
}

String PersonalityEngine::personalizeMessage(const String& baseMessage) {
  String personalized = baseMessage;
  personalized.replace("{name}", userName);
  return personalized;
}

void PersonalityEngine::setMood(MoodType mood) {
  if (currentMood != mood) {
    Logger::info("💭 Mood change: " + getMoodString() + " -> " + String(mood));
    currentMood = mood;
  }
}

String PersonalityEngine::getMoodString() const {
  switch (currentMood) {
    case MOOD_HAPPY: return "Happy";
    case MOOD_CARING: return "Caring";
    case MOOD_CONCERNED: return "Concerned";
    case MOOD_WORRIED: return "Worried";
    case MOOD_SLEEPING: return "Sleeping";
    case MOOD_CELEBRATING: return "Celebrating";
    default: return "Unknown";
  }
}

void PersonalityEngine::updateMood(const BehaviorData& behavior) {
  MoodType newMood = PersonalityTraits::behaviorToMood(behavior);
  setMood(newMood);
  
  // Adjust caring intensity based on behavior urgency
  float urgency = PersonalityTraits::calculateCaringUrgency(behavior);
  caringIntensity = urgency;
  
  // Escalate care level if needed
  if (urgency > 0.7 && currentCareLevel < CARE_WORRIED) {
    escalateCareLevel();
  } else if (urgency < 0.3 && currentCareLevel > CARE_GENTLE) {
    reduceCareLevel();
  }
}

void PersonalityEngine::queueMessage(const String& message) {
  if (messageQueue.size() < 10) { // Limit queue size
    messageQueue.push_back(message);
  }
}

void PersonalityEngine::queueMessage(ResponseType type) {
  String message = generateCaringResponse(type);
  if (!message.isEmpty()) {
    queueMessage(message);
  }
}

String PersonalityEngine::getNextMessage() {
  if (messageQueue.empty()) {
    return "";
  }
  
  String message = messageQueue[0];
  messageQueue.erase(messageQueue.begin());
  return message;
}

void PersonalityEngine::recordUserResponse(ResponseType responseType, bool effective) {
  history.userResponded = true;
  history.consecutiveIgnored = 0;
  
  if (learningEnabled) {
    adaptToUser(responseType, effective ? 1.0 : 0.0);
  }
  
  // If user responded positively, reduce care level slightly
  if (effective && currentCareLevel > CARE_GENTLE) {
    reduceCareLevel();
  }
}

void PersonalityEngine::recordUserIgnored(ResponseType responseType) {
  history.userResponded = false;
  history.consecutiveIgnored++;
  
  if (learningEnabled) {
    adaptToUser(responseType, 0.2); // Low effectiveness for ignored messages
  }
  
  // If user consistently ignores, escalate care level
  if (history.consecutiveIgnored >= 3 && currentCareLevel < CARE_WORRIED) {
    escalateCareLevel();
  }
}

void PersonalityEngine::adaptToUser(ResponseType type, float effectiveness) {
  if (type < RESPONSE_COUNT) {
    // Exponential moving average
    userPreferences[type] = userPreferences[type] * (1.0 - adaptationRate) + 
                           effectiveness * adaptationRate;
  }
}

void PersonalityEngine::escalateCareLevel() {
  if (currentCareLevel < CARE_WORRIED) {
    currentCareLevel = (CareLevel)(currentCareLevel + 1);
    Logger::info("💚 Escalating care level to: " + String(currentCareLevel));
  }
}

void PersonalityEngine::reduceCareLevel() {
  if (currentCareLevel > CARE_GENTLE) {
    currentCareLevel = (CareLevel)(currentCareLevel - 1);
    Logger::info("🌱 Reducing care level to: " + String(currentCareLevel));
  }
}

bool PersonalityEngine::canRespondNow() const {
  return canRespond && (millis() - lastMessageTime > responseCooldown);
}

String PersonalityEngine::getPersonalityStatus() const {
  String status = "Mood: " + getMoodString();
  status += ", Care Level: " + String(currentCareLevel);
  status += ", Warmth: " + String(personalityWarmth);
  status += ", Ignored: " + String(history.consecutiveIgnored);
  return status;
}

void PersonalityEngine::setUserName(const String& name) {
  userName = name;
  Logger::info("👋 User name set to: " + userName);
}

// Namespace implementation for personality traits
namespace PersonalityTraits {
  
String getCaringPhrase(CareLevel level) {
  switch (level) {
    case CARE_GENTLE:
      return "gently suggests";
    case CARE_ENCOURAGING:
      return "encouragingly reminds you";
    case CARE_CONCERNED:
      return "is concerned and asks";
    case CARE_WORRIED:
      return "is really worried and insists";
    default:
      return "cares about you";
  }
}

MoodType behaviorToMood(const BehaviorData& behavior) {
  if (behavior.inactivityMinutes > URGENT_INACTIVITY_THRESHOLD) {
    return MOOD_WORRIED;
  } else if (behavior.inactivityMinutes > CONCERNED_INACTIVITY_THRESHOLD) {
    return MOOD_CONCERNED;
  } else if (behavior.hasPositiveBehavior) {
    return MOOD_CELEBRATING;
  } else if (behavior.needsSupport) {
    return MOOD_CARING;
  } else {
    return MOOD_HAPPY;
  }
}

float calculateCaringUrgency(const BehaviorData& behavior) {
  float urgency = 0.0;
  
  // Time-based urgency
  if (behavior.inactivityMinutes > URGENT_INACTIVITY_THRESHOLD) {
    urgency += 0.8;
  } else if (behavior.inactivityMinutes > CONCERNED_INACTIVITY_THRESHOLD) {
    urgency += 0.5;
  } else if (behavior.inactivityMinutes > NORMAL_INACTIVITY_THRESHOLD) {
    urgency += 0.3;
  }
  
  // Need-based urgency
  if (behavior.needsHydration) urgency += 0.3;
  if (behavior.needsMovement) urgency += 0.2;
  if (behavior.needsPostureAdjustment) urgency += 0.1;
  
  return min(urgency, 1.0);
}

}