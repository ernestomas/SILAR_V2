#include <Stepper.h>            //Librer\'ia del Adafruit Motor Shield V1
#include <AFMotor.h>            //Librer\'i interna de Arduino para Stepers

AF_Stepper plate(200, 1);       //Nombre del motor(pasos por vueltas, a la puerta M1 M2)
AF_Stepper crane(50, 2);        //Nombre del motor(pasos por vueltas, a la puerta M3 M4)

int pasos_base;
int pasos_crane;
int initial_position_base = 0;
int initial_position_crane = 0;
int initial_position = 0;



void setup()
{  
   Serial.begin(9600);           //Comunicaci\'on serial con la PC
      delay(30);                 //Esperar 30 milisegundos
      crane.setSpeed(50);        //Define velocidad de giro en rpm de la grua
      plate.setSpeed(6);         //Define velocidad de giro en rpm de la base
}

void loop(){
  if (Serial.available()){
    String orden = Serial.readString();                              //lee la orden 
    //Serial.println(orden);
    int cor = orden.indexOf("[");
    int dob = orden.indexOf(":");
    String dif = orden.substring(cor+1,dob);

    if (dif == "M"){
      int sep1 = orden.indexOf("/");
      int pos = orden.substring(dob+1,sep1).toInt();
      //Serial.println(pos);
      int sep2 = orden.indexOf("/",sep1+1);
      int base = orden.substring(sep1+1,sep2).toInt();                //Movimiento de la base.  
      //Serial.println(base); 
      int sep3 = orden.indexOf("/",sep2+1);
      int crane_step = orden.substring(sep2+1,sep3).toInt();          //Movimiento de la grua.
      //Serial.println(crane_step);
      //Serial.println("Posicion inicial "+String(initial_position)+"posicion actual "+String(pos));
     
      if (initial_position != pos){
            crane.step(initial_position_crane, FORWARD, MICROSTEP);   
            delay(30);
        
        //Serial.println("la base da "+String(i)+" hacia atras posicion");
        //plate.step(initial_position_base, BACKWARD, SINGLE);
        //Serial.println("la grua da "+String(i)+" hacia atras posicion");
        //Serial.println("base dio "+String(initial_position_crane)+" hacia atras y la grua dio "+String(initial_position_base));
        delay(500);
        initial_position_crane = 0;
        initial_position = pos;
      }

      pasos_base = base - initial_position_base;
      //Serial.println("la posicion inicial de la base es " +String(initial_position_base));
      initial_position_base = base;
      //Serial.println("los pasos que da la base son " +String(pasos_base));
      pasos_crane = crane_step - initial_position_crane;
      //Serial.println("la posicion inicial de la grua es " +String(initial_position_crane));
      initial_position_crane = crane_step;
      //Serial.println("los pasos que da la grua son " +String(pasos_crane));
    
    
      if (pasos_base == 0){
        delay(30);
      }else if (pasos_base > 0){
            plate.step(pasos_base, FORWARD, SINGLE);   
            delay(30);
        
        //Serial.println("la base da "+String(j)+" hacia adelante");
        //Serial.println("base hacia adelante "+String(pasos_base));  
      }else if (pasos_base < 0){
            plate.step(abs(pasos_base), BACKWARD, SINGLE);  
            delay(30);
        
        //Serial.println("la base da "+String(j)+" hacia atras");
        //Serial.println("base hacia atras "+String(pasos_base));  
      }

      if (pasos_crane == 0){
        delay(30);
      }else if (pasos_crane > 0){
          crane.step(pasos_crane, BACKWARD, MICROSTEP); 
          delay(30);
         
        
        //Serial.println("la grua da "+String(j)+" hacia adelante");
        //Serial.println("grua hacia adelante "+String(pasos_crane));    
      }else if (pasos_crane < 0){
          crane.step(abs(pasos_crane), FORWARD, MICROSTEP); 
          delay(30);
        
        
        //Serial.println("la grua da "+String(j)+" hacia atras");
        //Serial.println("grua hacia atras "+String(pasos_crane));  
      }
    }else if (dif == "A"){

      if (initial_position_crane == 0){
          delay(30);
      }else if (initial_position_crane > 0){
          crane.step(initial_position_crane, FORWARD, MICROSTEP); 
          initial_position_crane = 0;
          delay(30);    
      }

      if (initial_position_base == 0){
          delay(30);
      }else if (initial_position_base > 0){
          plate.step(initial_position_base, BACKWARD, SINGLE);   
          initial_position_base = 0;
          delay(30);
        
      }

      
          
    }else if (dif == "S"){
      if (initial_position_crane == 0){
          delay(30);
      }else if (initial_position_crane > 0){
          crane.step(initial_position_crane, FORWARD, MICROSTEP); 
          initial_position_crane = 0;
          delay(30);    
      }

      if (initial_position_base == 0){
          delay(30);
      }else if (initial_position_base > 0){
          plate.step(initial_position_base, BACKWARD, SINGLE);   
          initial_position_base = 0;
          delay(30);
        
      }
      initial_position_base = 0;
      int sep1 = orden.indexOf("/");
      int workstations = orden.substring(dob+1,sep1).toInt();                 //numero de estaciones de trabajo
      int sep2 = orden.indexOf("/",sep1+1);
      int ciclos = orden.substring(sep1+1,sep2).toInt();                      //numero de ciclos
      int sep3 = orden.indexOf("/",sep2+1);
      String posiciones = orden.substring(sep2+1,sep3);
      int f_posiciones[workstations];                                         //pasos de la base
      fun(workstations, posiciones, f_posiciones);
      int sep4 = orden.indexOf("/",sep3+1);
      String alturas = orden.substring(sep3+1,sep4);
      int f_alturas[workstations];
      fun(workstations, alturas, f_alturas);                                  //pasos de la grua
      int sep5 = orden.indexOf("/",sep4+1);
      String velocity = orden.substring(sep4+1,sep5);
      int f_velocity[workstations];
      fun_speed(workstations, velocity, f_velocity);                          //velocidades
      int sep6 = orden.indexOf("/",sep5+1);
      String velocity_extra = orden.substring(sep5+1,sep6);
      int f_velocity_extra[workstations];
      fun_speed(workstations, velocity_extra, f_velocity_extra); 
      int sep7 = orden.indexOf("/",sep6+1);
      String times = orden.substring(sep6+1,sep7);
      unsigned long f_times[workstations];
      fun_times(workstations, times, f_times);                                       //tiempos

      //Serial.println("la grua da "+String(j)+" hacia atras");
      
      
      for (int j=0;j<ciclos; j++){
        int camino_base = 0;
        for (int i=0; i<workstations; i++){
          if((f_posiciones[i]-camino_base)>0){
            plate.step(abs(f_posiciones[i]-camino_base), FORWARD, SINGLE);
          }else if((f_posiciones[i]-camino_base)<0){
            plate.step(abs(f_posiciones[i]-camino_base), BACKWARD, SINGLE);
          }
           
          delay(30);
          
          //Serial.println("la base da "+String(f_posiciones[i]-camino_base)+" hacia adelante "+ String(abs(f_posiciones[i]-camino_base)));

          
          crane.setSpeed(f_velocity[i]);
          crane.step(abs(f_alturas[i]), BACKWARD, MICROSTEP);
          delay(30);
          
          //Serial.println("la grua da "+String(j)+" hacia atras");
          //Serial.println("la grua da "+String(f_alturas[i])+" hacia adelante");
          delay(1000*f_times[i]);    
          crane.setSpeed(f_velocity_extra[i]);
          crane.step(abs(f_alturas[i]), FORWARD, MICROSTEP);
          delay(30);
          
          
          //Serial.println("la grua da "+String(j)+" hacia atras");
          //Serial.println("la grua da "+String(f_alturas[i])+" hacia atras");
          camino_base = f_posiciones[i];
          String bar = String(i)+":"+workstations+"/"+ j + ":" + ciclos;
          Serial.println(bar);
        }
        delay(1000);

        plate.step(abs(f_posiciones[workstations-1]), BACKWARD, SINGLE);
        delay(30);
        
        //Serial.println("la grua da "+String(j)+" hacia atras");
        //Serial.println("la base da "+String(f_posiciones[workstations-1])+" hacia atras");
      }
    }
  }
}

void fun(int num, String list, int list2[]){      //Funci\'on para convertir cadena de caracteres en lista
  int pos=0;
  for (int i = 0; i<num; i++){
    int coma = list.indexOf(",",pos+1);
    list2[i]=list.substring(pos+1,coma).toInt(); 
    pos = coma;
  }
}

void fun_times(int num, String list, unsigned long list2[]){      //Funci\'on para convertir cadena de caracteres en lista
  int pos=0;
  for (int i = 0; i<num; i++){
    int coma = list.indexOf(",",pos+1);
    list2[i]=strtoul(list.substring(pos+1,coma).c_str(), NULL, 10);
    pos = coma;
  }
}

void fun_speed(int num, String list, int list2[]){      //Funci\'on para convertir de velocidad en mm/seg a rad/seg
  int pos=0;
  for (int i = 0; i<num; i++){
    int coma = list.indexOf(",",pos+1);
    float vel = list.substring(pos+1,coma).toFloat(); 
    list2[i] = int(3.143788567*vel);
    pos = coma;
  }
}
