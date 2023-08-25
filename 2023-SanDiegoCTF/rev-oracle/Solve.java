public class Solve
{
    private static final int FLAG_LENGTH = 42;
    private static byte[] Decrypted = {48, 6, 122, -86, -73, -59, 78, 84, 105, 
                                    -119, -36, -118, 70, 17, 101, -85, 55, 
                                    -38, -91, 32, -18, -107, 53, 99, -74, 
                                    67, 89, 120, -41, 122, -100, -70, 34, 
                                    -111, 21, -128, 78, 27, 123, -103, 36, 87 };
    
    private static void firstPass() {
        for (int i = 0; i < 42; ++i) {
            final byte[] numbers = Solve.Decrypted;
            final int n = i;
            numbers[n] ^= (byte)(3 * i * i + 5 * i + 101 + i % 2);
        }
    }
    
    private static void secondPass() {
        final byte[] numbers = new byte[42];
        for (int i = 0; i < 42; ++i) {
            numbers[i] = (byte)((Solve.Decrypted[(i + 42 + 1) % 42] & 0xFF) >> 4 | (Solve.Decrypted[i] & 0xFF) << 4);
        }
        Solve.Decrypted = numbers;
    }
    
    private static void thirdPass() {
        for (int i = 0; i < 42; ++i) {
            final byte[] numbers = Solve.Decrypted;
            final int n = i;
            numbers[n] -= (byte)(7 * i * i + 31 * i + 127 + i % 2);
        }
    }
    
    public static void main(final String[] array) {
        thirdPass();
        secondPass();
        firstPass();
        for(int i = 0; i < 42; i++){
            System.out.print((char) Solve.Decrypted[i]);
        }
    }        
} 