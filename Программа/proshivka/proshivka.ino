//---------------------------------------
//-----LIBS, PINS, CONST & VARIABLES-----
//---------------------------------------
#include <EEPROM.h>

#define pin_motor_dir 7
#define pin_pump_dir 8
#define pin_motor_speed 9
#define pin_pump_speed 10

#define pin_motor_enc_phase_a 2
#define pin_motor_enc_phase_b 4
#define pin_pump_enc_phase_a 3

volatile int64_t motor_ticks = 0;
volatile int64_t pump_ticks = 0;

const double K_TICKS_CM = 0;
const double K_TICKS_ML = 0;

bool DISARM = 0;

struct settings {
  uint8_t depth = 0; // in cm.
  uint8_t volume = 0; // in ml.
}

//---------------------------------------
//-------------LOW LEVEL FUNC------------
//---------------------------------------

void Update_motor_enc() {
  if (digitalRead(pin_motor_enc_phase_b)) {
    motor_ticks++;
  } else {
    motor_ticks--;
  }
}
void Update_pump_enc() {
  motor_ticks++;
}

double P_regulator(int32_t x, double pk) {
  return x * pk;
}

void setup() {
  attachInterrupt(digitalPinToInterrupt(pin_motor_enc_phase_a), Update_motor_enc, RISING);
  attachInterrupt(digitalPinToInterrupt(pin_pump_enc_phase_a), Update_pump_enc, RISING);

  pinMode(pin_motor_dir, OUTPUT);
  pinMode(pin_pump_dir, OUTPUT);
  pinMode(pin_motor_speed, OUTPUT);
  pinMode(pin_pump_speed, OUTPUT);

  pinMode(pin_motor_enc_phase_a, INPUT);
  pinMode(pin_motor_enc_phase_b, INPUT);
  pinMode(pin_pump_enc_phase_a, INPUT);

  Serial.begin();
}

void Setup_motor(int speed) {
  analogWrite(pin_motor_speed, constrain(abs(speed), 0, 255));
  digitalWrite(pin_motor_dir, speed > 0);
}
void Setup_pump(int speed) {
  analogWrite(pin_pump_speed, constrain(abs(speed), 0, 255));
  digitalWrite(pin_pump_dir, speed > 0);
}

void save_settings() {
  EEPROM.put(0, settings);
}
void read_settings() {
  EEPROM.get(0, settings);
}

//---------------------------------------
//------------HIGH LEVEL FUNC------------
//---------------------------------------

void Move_motor_ticks(int64_t ticks, int speed) {
  int64_t start_ticks = motor_ticks;
  Setup_motor(speed );
  while (motor_ticks - start_ticks < ticks) {}
  Setup_motor(0);
}

void Move_pump_ticks(int64_t ticks, int speed) {
  int64_t start_ticks = pump_ticks;
  Setup_pump(speed);
  while (pump_ticks - start_ticks < ticks) {}
  Setup_pump(0);
}
void input_data() {
  if (Serial.available()) {
    DISARM = 1;

    char key = Serial.read();
    int val = Serial.parseInt();
    switch (key) {
      case 'd':
        settings.depth = val;
        break;
      case 'v':
        settings.volume = val;
        break;
    }

    DISARM = 0;
    return;
  }
}

//---------------------------------------
//---------------MAIN CODE---------------
//---------------------------------------

void loop() {

}
