strings -n 8 flag | grep -i "UPX"
echo "download upx here https://upx.github.io/"
./upx -d -o flag_unpacked flag 
echo "next debug it with gdb"