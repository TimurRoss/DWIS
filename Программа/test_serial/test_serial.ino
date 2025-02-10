void setup() {
    // Начинаем работу с Serial портом на скорости 9600 бит/с
    Serial.begin(9600);
}
void loop() {
    // Проверяем, есть ли данные из Serial порта
    if (Serial.available() > 0) {
        // Читаем полученные данные и сохраняем их в переменной
        String receivedData = Serial.readString();
        // Отправляем ответ обратно в Serial порт
        Serial.println("Received: " + receivedData);
    }
}