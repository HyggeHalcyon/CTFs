import java.util.*;

class Solve {
    public static void main(String args[]) {
        char[] buffer = new char[32];
        byte[] myBytes = {
            0x3b, 0x65, 0x21, 0xa , 0x38, 0x0 , 0x36, 0x1d,
            0xa , 0x3d, 0x61, 0x27, 0x11, 0x66, 0x27, 0xa ,
            0x21, 0x1d, 0x61, 0x3b, 0xa , 0x2d, 0x65, 0x27,
            0xa , 0x6c, 0x60, 0x37, 0x30, 0x60, 0x31, 0x36,
        };
        for (int i=0; i<32; i++) {
            buffer[i] = (char) (myBytes[i] ^ 0x55);
        }
        
        // somehow concatinate it with string brokes it
        System.out.println("picoCTF{" + buffer + "}");
        System.out.print("picoCTF{");
        System.out.print(buffer);
        System.out.println("}");
    }
}