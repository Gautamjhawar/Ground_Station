char q;
bool setsupply= false;
bool setcda= false;
String valsetsupply=" %";
String valsetcda=" %";
bool token=false;
void(* resetFunc) (void) = 0; //declare reset function @ address 0
void setup() {
  Serial.begin(57600);// put your setup code here, to run once:

}

void loop() {

  // put your main code here, to run repeatedly:
    String s="A%";
    s+=String(random(75,150))+"%"; 
    if(Serial.available()>0 || token==true){
    q=Serial.read();
    if(q=='r'||q=='R')
    {
      resetFunc();
    }
    token=true;
    if(setsupply==false){
      if(q=='H' || q=='h')
      {
          valsetsupply=String(random(75,150))+"%";
          s+=valsetsupply;
          s+="D%";
          setsupply=true;
      }
      else{
          s+="Na%";
          s+="E%";
      }
    }
    else{
       s+=valsetsupply;
          s+="D%";
    }
    if(setcda==false){ 
        if(q=='s' ||q=='S')
        {
            valsetcda=String(random(75,150))+"%";
            s+=valsetcda;
            s+="D%";
            setcda=true;
        }
        else{
            s+="Na%";
            s+="E%";
        } 
    } 
    else{
          s+=valsetcda;
            s+="D%";
    }
}
    else{
       s+="Na%E%Na%E";
    }
    Serial.println(s);
    delay(1000);
}
