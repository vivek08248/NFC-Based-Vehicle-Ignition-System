#include <WiFi.h>
#include <esp_wifi.h>

const char* ssid = "NFC_ESP32";
const char* password = "Vivek123";
bool wasConnected = false;

void setup() {
  Serial.begin(115200);
  delay(1000);
  WiFi.softAP(ssid, password);
  Serial.println("NFC_SYSTEM_READY");
}

void loop() {
  int clientCount = WiFi.softAPgetStationNum();
  
  if (clientCount > 0 && !wasConnected) {
    wasConnected = true; // Mark as connected immediately
    
    // Wait exactly 1 second for the phone's MAC to register on the network
    delay(1000); 
    
    wifi_sta_list_t stationList;
    esp_err_t err = esp_wifi_ap_get_sta_list(&stationList);
    
    // ALWAYS print the trigger word first so Python definitely catches it
    Serial.print("USER_PRESENT MAC:");
    
    // Try to append the MAC address
    if (err == ESP_OK && stationList.num > 0) {
      for(int i = 0; i < 6; i++){
        Serial.printf("%02X", stationList.sta[0].mac[i]);
        if(i < 5) Serial.print(":");
      }
    } else {
      Serial.print("UNKNOWN");
    }
    
    // Crucial: Send the hidden "Enter" key so Python knows the line is finished
    Serial.println(); 
  } 
  else if (clientCount == 0 && wasConnected) {
    Serial.println("WAITING");
    wasConnected = false;
  }
  
  delay(500); // Check the network twice a second
}