package main

import (
	"encoding/base64"
	"fmt"
	"log"
)

const KEY = "123456789123" //152587890625762939453125"
const ENCODED = "VFFbWxUUQ1BcEVBaQ1YTXUYWUUpcVBwRO1dLXUE8UltRXhIRd35yc05dBlRVbkZEAEZHB0dpRAxPVG1HWQFsQwVEW1xEEzg="

func main() {
	decoded, err := base64.StdEncoding.DecodeString(ENCODED)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("[+] DECODED:", decoded)

	var decrypted []byte
	for idx, val := range decoded {
		decrypted = append(decrypted, val^KEY[idx%len(KEY)])
	}
	fmt.Println("[+] DECRYPTED:", string(decrypted))
}
