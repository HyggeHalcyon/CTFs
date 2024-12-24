- uses [rpmalloc](https://github.com/mjansson/rpmalloc)  
- [rpmalloc common attacks](https://blog.infosectcbr.com.au/2019/12/attacks-on-tcmalloc-heap-allocator.html)  

- [llvm rpmalloc](https://llvm.org/doxygen/md_lib_Support_rpmalloc_README.html), quote "The allocator is similar in spirit to tcmalloc from the [Google Performance Toolkit](https://github.com/gperftools/gperftools)."  
i.e [TCmalloc](https://goog-perftools.sourceforge.net/doc/tcmalloc.html)

- difference from rpmalloc is "Unlike tcmalloc, single blocks do not flow between threads, only entire spans of pages."

- which in turn uses kind of similar terms such as `run` and `regions` to [Jemalloc](https://0xten.gitbook.io/public/pwn/heap/jemalloc), tldr of the term can be seen in [Ancient-House](https://blog.bi0s.in/2021/08/15/Pwn/InCTFi21-AncientHouse/) writeup.

- quote from [pwn747](https://david942j.blogspot.com/2017/06/write-up-google-ctf-2017-pwn474-primary.html), "tcmalloc doesn't do any security check, fake any pointers can do the magic.", which I also assume for rpmalloc