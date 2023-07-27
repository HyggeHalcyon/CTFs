import java.util.*;

class Solve{
    public static void main(String[] Args){
        char[] buffer = new char[32];

        byte[] myBytes = {
            106 , 85  , 53  , 116 , 95  , 52  , 95  , 98  ,
            0x55, 0x6e, 0x43, 0x68, 0x5f, 0x30, 0x66, 0x5f,
            0142, 0131, 0164, 063 , 0163, 0137, 0143, 061 ,
            '9' , '4' , 'f' , '7' , '4' , '5' , '8' , 'e' ,
        };

        for (int i=0; i<32; i++) {
            buffer[i] = (char) (myBytes[i] & 0xFF);
        }
        
        // somehow concatinate it with string brokes it
        System.out.println("picoCTF{" + buffer + "}");
        System.out.print("picoCTF{");
        System.out.print(buffer);
        System.out.println("}");
    }
}