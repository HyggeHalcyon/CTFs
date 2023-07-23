// 
// Decompiled by Procyon v0.5.36
// 

public class Oracle
{
    private static final int FLAG_LENGTH = 42;
    private static final byte[] CHECK;
    private static byte[] numbers;
    
    private static void firstPass() {
        for (int i = 0; i < 42; ++i) {
            final byte[] numbers = Oracle.numbers;
            final int n = i;
            numbers[n] ^= (byte)(3 * i * i + 5 * i + 101 + i % 2);
        }
    }
    
    private static void secondPass() {
        final byte[] numbers = new byte[42];
        for (int i = 0; i < 42; ++i) {
            numbers[i] = (byte)(Oracle.numbers[(i + 42 - 1) % 42] << 4 | (Oracle.numbers[i] & 0xFF) >> 4);
        }
        Oracle.numbers = numbers;
    }
    
    private static void thirdPass() {
        for (int i = 0; i < 42; ++i) {
            final byte[] numbers = Oracle.numbers;
            final int n = i;
            numbers[n] += (byte)(7 * i * i + 31 * i + 127 + i % 2);
        }
    }
    
    private static void fail() {
        System.out.println("That's not the flag. Try again.");
        System.exit(1);
    }
    
    public static void main(final String[] array) {
        Oracle.numbers = System.console().readLine("Enter flag: ", new Object[0]).getBytes();
        if (Oracle.numbers.length != 42) {
            fail();
        }
        firstPass();
        secondPass();
        thirdPass();
        int n = 0;
        for (int i = 0; i < 42; ++i) {
            n |= (Oracle.CHECK[i] ^ Oracle.numbers[i]);
        }
        if (n != 0) {
            fail();
        }
        System.out.println("Good job. You found the flag!");
    }
    
    static {
        CHECK = new byte[] { 48, 6, 122, -86, -73, -59, 78, 84, 105, -119, -36, -118, 70, 17, 101, -85, 55, -38, -91, 32, -18, -107, 53, 99, -74, 67, 89, 120, -41, 122, -100, -70, 34, -111, 21, -128, 78, 27, 123, -103, 36, 87 };
    }
}

