/*
 * Pixel Plant - Camera Test
 * 
 * Tests the OV2640 camera module functionality
 * Verifies camera initialization and image capture
 * 
 * Hardware: ESP32-S3 FireBeetle with integrated OV2640 camera
 * Note: Camera pins are predefined in the FireBeetle board
 */

#include "esp_camera.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

// Camera configuration for DFRobot FireBeetle ESP32-S3
// These pins are specific to the FireBeetle board
#define PWDN_GPIO_NUM     -1   // Power down (not used on FireBeetle)
#define RESET_GPIO_NUM    -1   // Reset (not used on FireBeetle)
#define XCLK_GPIO_NUM     45   // Clock
#define SIOD_GPIO_NUM     1    // SDA (I2C data)
#define SIOC_GPIO_NUM     2    // SCL (I2C clock)

#define Y9_GPIO_NUM       48   // Data pins
#define Y8_GPIO_NUM       46
#define Y7_GPIO_NUM       8
#define Y6_GPIO_NUM       7
#define Y5_GPIO_NUM       4
#define Y4_GPIO_NUM       41
#define Y3_GPIO_NUM       40
#define Y2_GPIO_NUM       39

#define VSYNC_GPIO_NUM    6    // Vertical sync
#define HREF_GPIO_NUM     42   // Horizontal reference
#define PCLK_GPIO_NUM     5    // Pixel clock

// Test parameters
int currentTest = 0;
unsigned long lastTestTime = 0;
unsigned long testInterval = 10000; // Test every 10 seconds
int captureCount = 0;
bool cameraInitialized = false;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Disable brownout detector (can cause camera issues)
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  
  Serial.println("\n🌿 Pixel Plant Camera Test Starting...");
  Serial.println("=====================================");
  Serial.println("Hardware: DFRobot FireBeetle ESP32-S3");
  Serial.println("Camera: OV2640 2MP");
  Serial.println("=====================================\n");
  
  // Initialize camera
  if (initializeCamera()) {
    Serial.println("✅ Camera initialized successfully!");
    cameraInitialized = true;
    
    // Print camera info
    printCameraInfo();
    
    Serial.println("\n📋 Test Sequence:");
    Serial.println("• Basic image capture");
    Serial.println("• Image quality tests");
    Serial.println("• Different resolutions");
    Serial.println("• Frame rate testing");
    Serial.println("• Memory usage monitoring");
    Serial.println("\n🎯 Starting camera tests...");
    Serial.println("===========================================\n");
    
  } else {
    Serial.println("❌ Camera initialization failed!");
    Serial.println("\n🔧 Troubleshooting tips:");
    Serial.println("• Check if this is a FireBeetle ESP32-S3 with camera");
    Serial.println("• Verify the camera module is properly connected");
    Serial.println("• Try restarting the device");
    Serial.println("• Check for sufficient power supply");
  }
  
  lastTestTime = millis();
}

void loop() {
  if (!cameraInitialized) {
    delay(5000);
    Serial.println("⚠️ Camera not available - retrying initialization...");
    if (initializeCamera()) {
      cameraInitialized = true;
      Serial.println("✅ Camera recovery successful!");
    }
    return;
  }
  
  // Run tests at intervals
  if (millis() - lastTestTime > testInterval) {
    runCurrentTest();
    currentTest = (currentTest + 1) % 5; // 5 different tests
    lastTestTime = millis();
  }
  
  delay(1000); // Prevent tight loop
}

bool initializeCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  // Frame buffer settings
  config.frame_size = FRAMESIZE_QVGA; // 320x240 - good balance of quality/memory
  config.jpeg_quality = 12;           // 0-63, lower means higher quality
  config.fb_count = 2;                // Number of frame buffers
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  
  // Initialize camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("❌ Camera init failed with error 0x%x\n", err);
    return false;
  }
  
  // Get camera sensor
  sensor_t * s = esp_camera_sensor_get();
  if (s == NULL) {
    Serial.println("❌ Failed to get camera sensor");
    return false;
  }
  
  // Initial sensor settings for good image quality
  s->set_brightness(s, 0);     // -2 to 2
  s->set_contrast(s, 0);       // -2 to 2
  s->set_saturation(s, 0);     // -2 to 2
  s->set_special_effect(s, 0); // 0 to 6 (0=No Effect)
  s->set_whitebal(s, 1);       // 0 = disable , 1 = enable
  s->set_awb_gain(s, 1);       // 0 = disable , 1 = enable
  s->set_wb_mode(s, 0);        // 0 to 4 - if awb_gain enabled
  s->set_exposure_ctrl(s, 1);  // 0 = disable , 1 = enable
  s->set_aec2(s, 0);           // 0 = disable , 1 = enable
  s->set_ae_level(s, 0);       // -2 to 2
  s->set_aec_value(s, 300);    // 0 to 1200
  s->set_gain_ctrl(s, 1);      // 0 = disable , 1 = enable
  s->set_agc_gain(s, 0);       // 0 to 30
  s->set_gainceiling(s, (gainceiling_t)0);  // 0 to 6
  s->set_bpc(s, 0);            // 0 = disable , 1 = enable
  s->set_wpc(s, 1);            // 0 = disable , 1 = enable
  s->set_raw_gma(s, 1);        // 0 = disable , 1 = enable
  s->set_lenc(s, 1);           // 0 = disable , 1 = enable
  s->set_hmirror(s, 0);        // 0 = disable , 1 = enable
  s->set_vflip(s, 0);          // 0 = disable , 1 = enable
  s->set_dcw(s, 1);            // 0 = disable , 1 = enable
  s->set_colorbar(s, 0);       // 0 = disable , 1 = enable
  
  return true;
}

void printCameraInfo() {
  sensor_t * s = esp_camera_sensor_get();
  if (s != NULL) {
    camera_sensor_info_t * info = esp_camera_sensor_get_info(&(s->id));
    if (info != NULL) {
      Serial.printf("📷 Camera Model: %s\n", info->name);
      Serial.printf("📷 PID: 0x%02x\n", info->pid);
      Serial.printf("📷 VER: 0x%02x\n", info->ver);
    }
    
    // Get current frame size
    framesize_t framesize = s->status.framesize;
    Serial.printf("📷 Frame Size: %s\n", getFrameSizeName(framesize));
    Serial.printf("📷 JPEG Quality: %d\n", s->status.quality);
    Serial.printf("📷 Brightness: %d\n", s->status.brightness);
    Serial.printf("📷 Contrast: %d\n", s->status.contrast);
  }
  
  Serial.printf("📷 PSRAM Total: %d bytes\n", ESP.getPsramSize());
  Serial.printf("📷 PSRAM Free: %d bytes\n", ESP.getFreePsram());
}

const char* getFrameSizeName(framesize_t framesize) {
  switch(framesize) {
    case FRAMESIZE_96X96: return "96x96";
    case FRAMESIZE_QQVGA: return "QQVGA (160x120)";
    case FRAMESIZE_QCIF: return "QCIF (176x144)";
    case FRAMESIZE_HQVGA: return "HQVGA (240x176)";
    case FRAMESIZE_240X240: return "240x240";
    case FRAMESIZE_QVGA: return "QVGA (320x240)";
    case FRAMESIZE_CIF: return "CIF (400x296)";
    case FRAMESIZE_HVGA: return "HVGA (480x320)";
    case FRAMESIZE_VGA: return "VGA (640x480)";
    case FRAMESIZE_SVGA: return "SVGA (800x600)";
    case FRAMESIZE_XGA: return "XGA (1024x768)";
    case FRAMESIZE_HD: return "HD (1280x720)";
    case FRAMESIZE_SXGA: return "SXGA (1280x1024)";
    case FRAMESIZE_UXGA: return "UXGA (1600x1200)";
    default: return "Unknown";
  }
}

void runCurrentTest() {
  switch (currentTest) {
    case 0:
      testBasicCapture();
      break;
    case 1:
      testDifferentResolutions();
      break;
    case 2:
      testImageQuality();
      break;
    case 3:
      testFrameRate();
      break;
    case 4:
      testMemoryUsage();
      break;
  }
}

void testBasicCapture() {
  Serial.println("📸 Test 1/5: Basic Image Capture");
  
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("❌ Camera capture failed");
    return;
  }
  
  captureCount++;
  Serial.printf("✅ Capture #%d successful!\n", captureCount);
  Serial.printf("   Image size: %d x %d pixels\n", fb->width, fb->height);
  Serial.printf("   File size: %d bytes\n", fb->len);
  Serial.printf("   Format: %s\n", fb->format == PIXFORMAT_JPEG ? "JPEG" : "Other");
  Serial.printf("   Timestamp: %lu ms\n", millis());
  
  esp_camera_fb_return(fb);
  Serial.println();
}

void testDifferentResolutions() {
  Serial.println("📸 Test 2/5: Different Resolutions");
  
  framesize_t resolutions[] = {FRAMESIZE_QQVGA, FRAMESIZE_QVGA, FRAMESIZE_VGA};
  const char* resNames[] = {"QQVGA (160x120)", "QVGA (320x240)", "VGA (640x480)"};
  
  sensor_t * s = esp_camera_sensor_get();
  framesize_t originalSize = s->status.framesize;
  
  for (int i = 0; i < 3; i++) {
    Serial.printf("   Testing %s...\n", resNames[i]);
    
    s->set_framesize(s, resolutions[i]);
    delay(500); // Give camera time to adjust
    
    unsigned long startTime = millis();
    camera_fb_t * fb = esp_camera_fb_get();
    unsigned long captureTime = millis() - startTime;
    
    if (fb) {
      Serial.printf("   ✅ %s: %d x %d, %d bytes, %lu ms\n", 
                    resNames[i], fb->width, fb->height, fb->len, captureTime);
      esp_camera_fb_return(fb);
    } else {
      Serial.printf("   ❌ %s failed\n", resNames[i]);
    }
  }
  
  // Restore original resolution
  s->set_framesize(s, originalSize);
  Serial.println();
}

void testImageQuality() {
  Serial.println("📸 Test 3/5: Image Quality Settings");
  
  sensor_t * s = esp_camera_sensor_get();
  int originalQuality = s->status.quality;
  
  int qualities[] = {10, 20, 40}; // Lower = better quality
  const char* qualityNames[] = {"High", "Medium", "Low"};
  
  for (int i = 0; i < 3; i++) {
    Serial.printf("   Testing %s quality (JPEG quality %d)...\n", 
                  qualityNames[i], qualities[i]);
    
    s->set_quality(s, qualities[i]);
    delay(200);
    
    unsigned long startTime = millis();
    camera_fb_t * fb = esp_camera_fb_get();
    unsigned long captureTime = millis() - startTime;
    
    if (fb) {
      Serial.printf("   ✅ %s: %d bytes, %lu ms\n", 
                    qualityNames[i], fb->len, captureTime);
      esp_camera_fb_return(fb);
    } else {
      Serial.printf("   ❌ %s quality test failed\n", qualityNames[i]);
    }
  }
  
  // Restore original quality
  s->set_quality(s, originalQuality);
  Serial.println();
}

void testFrameRate() {
  Serial.println("📸 Test 4/5: Frame Rate Performance");
  
  int frameCount = 10;
  unsigned long startTime = millis();
  int successfulFrames = 0;
  
  Serial.printf("   Capturing %d frames...\n", frameCount);
  
  for (int i = 0; i < frameCount; i++) {
    camera_fb_t * fb = esp_camera_fb_get();
    if (fb) {
      successfulFrames++;
      esp_camera_fb_return(fb);
    }
    
    // Small delay to prevent overwhelming the system
    delay(10);
  }
  
  unsigned long totalTime = millis() - startTime;
  float fps = (successfulFrames * 1000.0) / totalTime;
  
  Serial.printf("   ✅ Captured %d/%d frames in %lu ms\n", 
                successfulFrames, frameCount, totalTime);
  Serial.printf("   📊 Frame rate: %.2f FPS\n", fps);
  Serial.printf("   📊 Average frame time: %.2f ms\n", 
                totalTime / (float)successfulFrames);
  Serial.println();
}

void testMemoryUsage() {
  Serial.println("📸 Test 5/5: Memory Usage Monitoring");
  
  size_t psramBefore = ESP.getFreePsram();
  size_t heapBefore = ESP.getFreeHeap();
  
  Serial.printf("   Memory before capture:\n");
  Serial.printf("     PSRAM Free: %d bytes\n", psramBefore);
  Serial.printf("     Heap Free: %d bytes\n", heapBefore);
  
  // Capture and hold multiple frames to test memory usage
  camera_fb_t * frames[3] = {NULL, NULL, NULL};
  
  for (int i = 0; i < 3; i++) {
    frames[i] = esp_camera_fb_get();
    if (frames[i]) {
      size_t psramNow = ESP.getFreePsram();
      size_t heapNow = ESP.getFreeHeap();
      Serial.printf("   After frame %d: PSRAM=%d, Heap=%d\n", 
                    i+1, psramNow, heapNow);
    }
  }
  
  // Return all frames
  for (int i = 0; i < 3; i++) {
    if (frames[i]) {
      esp_camera_fb_return(frames[i]);
    }
  }
  
  size_t psramAfter = ESP.getFreePsram();
  size_t heapAfter = ESP.getFreeHeap();
  
  Serial.printf("   Memory after cleanup:\n");
  Serial.printf("     PSRAM Free: %d bytes\n", psramAfter);
  Serial.printf("     Heap Free: %d bytes\n", heapAfter);
  
  if (psramAfter >= psramBefore && heapAfter >= heapBefore) {
    Serial.println("   ✅ No memory leaks detected");
  } else {
    Serial.println("   ⚠️ Possible memory usage issue");
  }
  
  Serial.println();
  Serial.println("===========================================");
}

// Function that can be called from main firmware
bool testCameraCapture() {
  if (!cameraInitialized) {
    Serial.println("❌ Camera not initialized");
    return false;
  }
  
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("❌ Camera capture test failed");
    return false;
  }
  
  Serial.printf("✅ Camera test passed: %dx%d, %d bytes\n", 
                fb->width, fb->height, fb->len);
  esp_camera_fb_return(fb);
  return true;
}