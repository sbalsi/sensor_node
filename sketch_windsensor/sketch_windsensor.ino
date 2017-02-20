/*
The sketch uses the on-chip temperature sensing thermistor to compensate the sensor
 for changes in ambient temperature. Because the thermistor is just configured as a
 voltage divider, the voltage will change with supply voltage. This is why the 
 sketch depends upon a regulated five volt supply.

Hardware Setup: 
 Wind Sensor Signals    Arduino
 GND                    GND
 +V                     5V
 RV                     A1   
 TMP                    A0 

*/

const int analogPinForRV =   1;  
const int analogPinForTMP =  0;

// to calibrate sensor, put a glass over it, but the sensor should not be
// touching the desktop surface however.
// adjust the zeroWindAdjustment until your sensor reads about zero with the glass over it. 

const float zeroWindAdjustment = 0.3; // -0.4 negative numbers yield smaller wind speeds and vice versa.

int TMP_Therm_ADunits;  //temp termistor value from wind sensor
float TMP_Therm_Volts;
float RV_Wind_ADunits;    //RV output from wind sensor 
float RV_Wind_Volts;
unsigned long lastMillis;
float TempCtimes100;
float Temp_Celsius;
float zeroWind_ADunits;
float zeroWind_volts;
float WindSpeed_MPH;


void setup() {
  
    Serial.begin(57600);
    pinMode(A2, INPUT);        // GND pin      
    pinMode(A3, INPUT);        // VCC pin
    digitalWrite(A3, LOW);     // turn off pullups
}

void loop() {
    
    if (millis() - lastMillis > 1000){      // In  ms 
    
    TMP_Therm_ADunits = analogRead(analogPinForTMP);
    TMP_Therm_Volts = TMP_Therm_ADunits * 0.0048828125;   
    RV_Wind_ADunits = analogRead(analogPinForRV);
    RV_Wind_Volts = (RV_Wind_ADunits *  0.0048828125);

    // these are all derived from regressions from raw data as such they depend on a lot of experimental factors
    // such as accuracy of temp sensors, and voltage at the actual wind sensor, (wire losses) which were unaccouted for.
    TempCtimes100 = (0.005 *((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits)) - (16.862 * (float)TMP_Therm_ADunits) + 9075.4;  
    Temp_Celsius = TempCtimes100/100 - 1.78;
    zeroWind_ADunits = -0.0006*((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172;  //  13.0C  553  482.39

    zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment;  

    // This from a regression from data in the form of 
    // Vraw = V0 + b * WindSpeed ^ c
    // V0 is zero wind at a particular temperature
    // The constants b and c were determined by some Excel wrangling with the solver.
    
   WindSpeed_MPH =  pow(((RV_Wind_Volts - zeroWind_volts) /.2300) , 2.7265);   
   
   //Format: TMP_volts\tTempC\rv_wind_volts\tZeroWind_volts\tWindSpeed\t      
   

   //Serial.println(TMP_Therm_Volts);
   //Serial.print("\t");
   //Serial.print(TempCtimes100);
   //Serial.print("\t");
   //Serial.print((float)RV_Wind_Volts);
   //Serial.print("\t");
   //Serial.print(zeroWind_volts);
   //Serial.print("\t");
   //Serial.println((float)WindSpeed_MPH);
   //Serial.print("\t");*/

   //Serial.println(TMP_Therm_Volts+","+TempCtimes100+","+(float)RV_Wind_Volts+","+zeroWind_volts+","+(float)WindSpeed_MPH);   

   Serial.print(TMP_Therm_Volts);
   Serial.print(",");
   Serial.print(Temp_Celsius);
   Serial.print(",");
   Serial.print((float)RV_Wind_Volts);
   Serial.print(",");
   Serial.print(zeroWind_volts);
   Serial.print(",");
   Serial.print((float)WindSpeed_MPH);
   Serial.print("\n");

   lastMillis = millis();

      
   /*
    Serial.print("  TMP volts ");
    Serial.print(TMP_Therm_ADunits * 0.0048828125);
    
    Serial.print(" RV volts ");
    Serial.print((float)RV_Wind_Volts);

    Serial.print("\t  TempC*100 ");
    Serial.print(TempCtimes100 );

    Serial.print("   ZeroWind volts ");
    Serial.print(zeroWind_volts);

    Serial.print("   WindSpeed MPH ");
    Serial.println((float)WindSpeed_MPH);
    lastMillis = millis(); 
    */
    
    
  } 
    
}


