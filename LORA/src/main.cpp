#include <SPI.h>
#include <LoRa.h>

// STM32 Nucleo F411RE pin definitions for LoRa module
// Using SPI1: SCK=PA5 (D13), MISO=PA6 (D12), MOSI=PA7 (D11)
#define ss PA4     // NSS (chip select) - D10 
#define rst PB0    // Reset pin - D8
#define dio0 PA1   // DIO0 pin - D2

//Frequency
#define LORA_FREQUENCY 433E6

int counter = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Sender - STM32 Nucleo F411RE");
  Serial.flush();
  
  // Print pin configuration for debugging
  Serial.println("Pin Configuration for STM32 Nucleo F411RE:");
  Serial.println("SS (NSS): PA4 (D10)");
  Serial.println("RST: PB0 (D8)"); 
  Serial.println("DIO0: PA1 (D2)");
  Serial.println("SPI1: SCK=PA5(D13), MISO=PA6(D12), MOSI=PA7(D11)");

  // Initialize SPI
  SPI.begin();
  Serial.println("SPI initialized");

  // Test SPI communication by trying to read version register
  Serial.println("Testing SPI communication...");
  pinMode(ss, OUTPUT);
  pinMode(rst, OUTPUT);
  
  // Reset the module
  digitalWrite(rst, LOW);
  delay(10);
  digitalWrite(rst, HIGH);
  delay(10);
  
  // Try to read the version register (0x42) - should return 0x12 for SX1276
  digitalWrite(ss, LOW);
  SPI.transfer(0x42 & 0x7F); // Read version register
  uint8_t version = SPI.transfer(0x00);
  digitalWrite(ss, HIGH);
  
  Serial.print("LoRa chip version: 0x");
  Serial.println(version, HEX);
  
  if (version == 0x12) {
    Serial.println("SX1276/77/78/79 detected");
  } else if (version == 0x22) {
    Serial.println("SX1272/73 detected");
  } else if (version == 0x00 || version == 0xFF) {
    Serial.println("ERROR: No response from LoRa module!");
    Serial.println("Possible issues:");
    Serial.println("- Module not powered (needs 3.3V)");
    Serial.println("- SPI wiring incorrect");
    Serial.println("- Faulty module");
    Serial.println("- Check connections:");
    Serial.println("  VCC -> 3.3V");
    Serial.println("  GND -> GND");
    Serial.println("  SCK -> PA5 (D13)");
    Serial.println("  MISO -> PA6 (D12)");
    Serial.println("  MOSI -> PA7 (D11)");
    Serial.println("  NSS -> PA4 (D10)");
    Serial.println("  RST -> PB0 (D8)");
    Serial.println("  DIO0 -> PA1 (D2)");
    while (1);
  } else {
    Serial.print("Unknown chip version: 0x");
    Serial.println(version, HEX);
  }

  // Set LoRa pins
  LoRa.setPins(ss, rst, dio0);

  Serial.print("Initializing LoRa at ");
  Serial.print(LORA_FREQUENCY / 1E6);
  Serial.println(" MHz...");
  
  if (!LoRa.begin(LORA_FREQUENCY)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  
  Serial.println("LoRa Initializing OK!");

  // Set the same Sync Word as the receiver
  LoRa.setSyncWord(0xF3);
  Serial.println("Sync Word set. Starting transmission...");
  
  // Optional: Set transmission power (2-20 for most modules)
  LoRa.setTxPower(20);
  Serial.println("TX Power set to 20dBm");
  
  // Optional: Set spreading factor (6-12, higher = longer range but slower)
  LoRa.setSpreadingFactor(7);
  Serial.println("Spreading Factor set to 7");
  
  // Optional: Set signal bandwidth (7.8, 10.4, 15.6, 20.8, 31.25, 41.7, 62.5, 125, 250, 500 kHz)
  LoRa.setSignalBandwidth(125E3);
  Serial.println("Signal Bandwidth set to 125 kHz");
  
  Serial.println("Ready to send packets!");
  
  // Add a small delay before starting the main loop
  delay(1000);
  Serial.println("Setup complete, starting main loop...");
}

void loop() {
  Serial.print("Sending packet: ");
  Serial.println(counter);
  Serial.flush(); // Ensure serial output is sent

  // Send packet with error checking
  Serial.println("Starting packet transmission...");
  
  if (LoRa.beginPacket()) {
    Serial.println("Packet begin successful");
    LoRa.print("Hello World #");
    LoRa.print(counter);
    
    if (LoRa.endPacket()) {
      Serial.print("Packet sent successfully: Hello World #");
      Serial.println(counter);
    } else {
      Serial.println("ERROR: Failed to send packet!");
    }
  } else {
    Serial.println("ERROR: Failed to begin packet!");
  }
  
  counter++;
  
  Serial.println("Entering delay...");
  Serial.flush(); // Ensure all output is sent before delay
  
  // Wait 2 seconds before sending next packet
  delay(2000); // Increased delay to 2 seconds
  
  Serial.println("Delay complete, looping...");
}
