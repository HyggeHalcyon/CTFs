
char* global_chunk = 0;
void module_ioctl(int fd,int cmd, char* args)

{
  long allocated_chunk;
  long lVar2;
  long idk;
  
  mutex_lock(&g_mutex);
  idk = global_chunk;
  if (cmd == 0x13370001) {
    if (
        (
            (global_chunk == 0) &&
            (allocated_chunk = kmalloc_trace_noprof(_DAT_001010a8,0x400cc0,0x1000), 
            idk = global_chunk, 
            allocated_chunk != 0)
        ) && 
        (
            lVar2 = _copy_from_user(allocated_chunk,args,0x1000), 
            idk = allocated_chunk, 
            lVar2 != 0
        )
        ) {
      kfree(allocated_chunk);
      idk = global_chunk;
    }
  }
  else if (cmd == 0x13370002) {
    kfree(global_chunk);
    idk = global_chunk;
  }
  global_chunk = idk;
  mutex_unlock(&g_mutex);
  __x86_return_thunk();
  return;
}

