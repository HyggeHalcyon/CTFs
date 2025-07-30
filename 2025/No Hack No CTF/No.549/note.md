Solves PoC: https://theori.io/blog/reviving-the-modprobe-path-technique-overcoming-search-binary-handler-patch

Quote:
> First, in kernel versions prior to v6.14-rc1, when a user attempts to execute a dummy file starting with a magic number such as \xff\xff\xff\xff  
> Last November, a patch removing legacy code from /fs/exec.c was merged into Upstream.  
> Looking at the diff of this patch, the flow that calls request_module() has been completely removed [4], so search_binary_handler() no longer invokes request_module().  

Basically a new way to invoke modprobe since the old way has been patched

other new ways trigger modprobe:
https://github.com/Naupjjin/2025-NHNC-CTF-challenge/tree/main/No549/solver 