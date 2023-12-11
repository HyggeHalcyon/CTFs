
### breakpoints
```
break *get_handle+23 memfd
break *main+39 dlsym
break *get_handle+213 dlopen
```

### important calls
```C
func get_handle(){
  /* other code */
  uint fd = memfd_create(":^)",0);

  for (i = 0; i < 0x3e08; i = i + 1) {
    tmp = __[i] ^ 55;
    write(fd,&tmp,1);
  }

  /* other code */

  sprintf((char *)&filename,"/proc/self/fd/%d",(ulong)fd);
  ret = dlopen(&filename,1);

  return ret;
}

func main(){
  /* other code */
  undefined8 handle = get_handle();
  code *addr = dlsym(handle,"_");

  /* other code */

  fgets(buffer,0x7f,stdin);
  idx = strcspn(buffer,"\n");
  buffer[idx] = '\0';
  check = (*addr)(buffer); // calling the external function

  /* other code */
}

```

### out.lib.sym['_']
```C
  local_48 = 0x743474737b425448;
  local_40 = 0x5f3562316c5f6331;
  local_38 = 0x6c3030635f747562;
  local_30 = 0x7d7233;
```