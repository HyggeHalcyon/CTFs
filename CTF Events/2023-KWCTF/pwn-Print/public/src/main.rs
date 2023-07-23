use libc;
use libc_stdhandle;

fn main() {
    unsafe {
        // init
        let stdin = libc_stdhandle::stdin();
        let stdout = libc_stdhandle::stdout();
        libc::setvbuf(stdout,&mut 0,libc::_IONBF,0);
        
        // setup flag
        let flag = [0 as libc::c_char; 41].as_mut_ptr();
        let fd = libc::fopen("flag.txt\0".as_ptr() as *const libc::c_char, "r\0".as_ptr() as *const libc::c_char);
        libc::fgets(flag, 40, fd);

        // input user
        let buff = [0 as libc::c_char; 32].as_mut_ptr();
        libc::printf("print \0".as_ptr() as *const libc::c_char);
        libc::fgets(buff,32,stdin);
        libc::printf(buff);
    }
}
