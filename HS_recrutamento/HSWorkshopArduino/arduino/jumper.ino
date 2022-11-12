int digit1 = 7;                                      // Set digit pins of the 4-digit 7 segment display
int digit2 = 4;
int digit3 = 3;
int digit4 = 19;

int segA = 6;                                        // Set segment pins of the 4-digit 7 segment display
int segB = 2;
int segC = 17;
int segD = 16;
int segE = 15;
int segF = 5;
int segG = 18;

int segA_lev = 10;                                   // Set segment pins of the 1-digit 7 segment display
int segB_lev = 9;
int segC_lev = 20;
int segD_lev = 14;
int segE_lev = 13;
int segF_lev = 11;
int segG_lev = 12;
                                 
int button = 8;                                      // Button input pin
bool invert_grav = false;
int player_y = 0;

unsigned long ms;
unsigned long time_counter;
unsigned long reset = 0;
int obj_digit;
int level = 1;
int slowdown = 6 - level;                            // Variable to change speed of obstacle for each level (1 <= level <= 5)
int counter = 0;

int obj_level = 0;

void setup() {
  pinMode(digit1, OUTPUT);
  pinMode(digit2, OUTPUT);
  pinMode(digit3, OUTPUT);
  pinMode(digit4, OUTPUT);
  
  pinMode(segA, OUTPUT);
  pinMode(segB, OUTPUT);
  pinMode(segC, OUTPUT);
  pinMode(segD, OUTPUT);
  pinMode(segE, OUTPUT);
  pinMode(segF, OUTPUT);
  pinMode(segG, OUTPUT);

  pinMode(segA_lev, OUTPUT);
  pinMode(segB_lev, OUTPUT);
  pinMode(segC_lev, OUTPUT);
  pinMode(segD_lev, OUTPUT);
  pinMode(segE_lev, OUTPUT);
  pinMode(segF_lev, OUTPUT);
  pinMode(segG_lev, OUTPUT);

  pinMode(button, INPUT);
  
  Serial.begin(9600);
}

void loop() {
  slowdown = 6 - level;
  if (digitalRead(button) == HIGH && counter == 0){  // Check for button press -> change gravity direction
    invert_grav = true;
    counter = 10;                                    // Counter to prevent button holding changing gravity every loop
  }
  if (digitalRead(button) == LOW && invert_grav){
    if (player_y == 0){
      player_y = 1;
    }
    else{
      player_y = 0;  
    }
    invert_grav = false;
  }
  if (counter > 0){
    counter--;
  }
  time_counter = millis();
  ms = millis() - reset;

  if ((ms % (400 * slowdown)) < (8 * slowdown)){     // Select random object height (0 -> floor; 1 -> ceiling)
    obj_level = random(2);
  }

  if ((ms % (400 * slowdown)) < (100 * slowdown)){   // Changing object coordinate depending on time -> moving obstacle
    obj_digit = 4;  
  }
  else if ((ms % (400 * slowdown)) >= (100 * slowdown) && (ms % (400 * slowdown)) < (200 * slowdown)){
    obj_digit = 3;
  }
  else if ((ms % (400 * slowdown)) >= (200 * slowdown) && (ms % (400 * slowdown)) < (300 * slowdown)){
    obj_digit = 2;
  }
  else if ((ms % (400 * slowdown)) >= (300 * slowdown) && (ms % (400 * slowdown)) < (400 * slowdown)){
    obj_digit = 1;
  }

  drawLevel(level);
  drawObs(obj_digit, obj_level);
  delay(1);
  drawPlayer(player_y);

  if (obj_digit == 1 && obj_level == player_y){      // Check for collision between player and obstacle
    level = 1;                                       // Reset to level 1 and reset timer
    reset = time_counter;
  }

  if (ms / 10000 > 0 && ms % 10000 < 5 && level < 5){
    level++;                                         // After 10 seconds without collision, advance to next level
  }

  delay(1);
}

void drawObs(int digit, int y){
  int digits[4] = {digit1, digit2, digit3, digit4};
  for (int i = 0; i <= 3; i = i + 1){                // Set all digit pins to HIGH except for the place we want to show the obstacle (ie. LOW HIGH HIGH HIGH -> obstacle on digit 1)
    if (i + 1 == digit){
      digitalWrite(digits[i], LOW);
    }
    else {
      digitalWrite(digits[i], HIGH);
    }
  }

  if (y == 0){                                       // y = 0 -> draw obstacle on floor, y = 1 -> draw obstacle on ceiling
    digitalWrite(segA, LOW);
    digitalWrite(segB, LOW);
    digitalWrite(segC, HIGH);
    digitalWrite(segD, HIGH);
    digitalWrite(segE, HIGH);
    digitalWrite(segF, LOW);
    digitalWrite(segG, HIGH); 
  }
  else{
    digitalWrite(segA, HIGH);
    digitalWrite(segB, HIGH);
    digitalWrite(segC, LOW);
    digitalWrite(segD, LOW);
    digitalWrite(segE, LOW);
    digitalWrite(segF, HIGH);
    digitalWrite(segG, HIGH);   
  }
 
}

void drawPlayer(bool jump){                          // Draw player on floor if jump = false or on ceiling if jump = true
  digitalWrite(digit1, LOW);
  digitalWrite(digit2, HIGH);
  digitalWrite(digit3, HIGH);
  digitalWrite(digit4, HIGH);

  if (jump){
    digitalWrite(segA, HIGH);
    digitalWrite(segB, HIGH);
    digitalWrite(segC, LOW);
    digitalWrite(segD, LOW);
    digitalWrite(segE, LOW);
    digitalWrite(segF, HIGH);
    digitalWrite(segG, HIGH);  
  }
  else{
    digitalWrite(segA, LOW);
    digitalWrite(segB, LOW);
    digitalWrite(segC, HIGH);
    digitalWrite(segD, HIGH);
    digitalWrite(segE, HIGH);
    digitalWrite(segF, LOW);
    digitalWrite(segG, HIGH);  
  }
    
}

void drawLevel(int lev){                             // Draw level number on left 7 segment display
  if (lev == 1){
    digitalWrite(segA_lev, LOW);
    digitalWrite(segB_lev, HIGH);
    digitalWrite(segC_lev, HIGH);
    digitalWrite(segD_lev, LOW);
    digitalWrite(segE_lev, LOW);
    digitalWrite(segF_lev, LOW);
    digitalWrite(segG_lev, LOW);
  }  
  else if (lev == 2){
    digitalWrite(segA_lev, HIGH);
    digitalWrite(segB_lev, HIGH);
    digitalWrite(segC_lev, LOW);
    digitalWrite(segD_lev, HIGH);
    digitalWrite(segE_lev, HIGH);
    digitalWrite(segF_lev, LOW);
    digitalWrite(segG_lev, HIGH);
  }
  else if (lev == 3){
    digitalWrite(segA_lev, HIGH);
    digitalWrite(segB_lev, HIGH);
    digitalWrite(segC_lev, HIGH);
    digitalWrite(segD_lev, HIGH);
    digitalWrite(segE_lev, LOW);
    digitalWrite(segF_lev, LOW);
    digitalWrite(segG_lev, HIGH);
  }
  else if (lev == 4){
    digitalWrite(segA_lev, LOW);
    digitalWrite(segB_lev, HIGH);
    digitalWrite(segC_lev, HIGH);
    digitalWrite(segD_lev, LOW);
    digitalWrite(segE_lev, LOW);
    digitalWrite(segF_lev, HIGH);
    digitalWrite(segG_lev, HIGH);
  }
  else if (lev == 5){
    digitalWrite(segA_lev, HIGH);
    digitalWrite(segB_lev, LOW);
    digitalWrite(segC_lev, HIGH);
    digitalWrite(segD_lev, HIGH);
    digitalWrite(segE_lev, LOW);
    digitalWrite(segF_lev, HIGH);
    digitalWrite(segG_lev, HIGH);
  }
}
