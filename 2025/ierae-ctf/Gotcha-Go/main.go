// go build -gcflags=-B
package main

import (
	"fmt"
	"os"
)

type Data interface {
	info(int)
	init(*MyStr)
	edit(int)
}

var l Data = &MyList{}

type MyStr struct {
	idx  int
	data [0x30]byte
}

type MyList struct {
	list [16]*MyStr
}

//go:noinline
func (s *MyStr) info(_ int) {
	os.Stdout.Write(s.data[:])
}

func (s *MyStr) init(_ *MyStr) {
	os.Stdin.Read(s.data[:])
	l.init(s)
}

//go:noinline
func (s *MyStr) edit(_ int) {
	os.Stdin.Read(s.data[:])
}

func (m *MyList) info(idx int) {
	m.list[idx].info(idx)
}

func (m *MyList) init(ptr *MyStr) {
	m.list[ptr.idx] = ptr
}

func (m *MyList) edit(idx int) {
	m.list[idx].edit(idx)
}

func main() {
	for {
		var choice int64
		fmt.Println("Option (1.Init, 2.Info, 3.Edit):")
		fmt.Scanf("%d%*c", &choice)
		fmt.Println("Idx):")
		var idx int
		switch choice {
		case 1:
			fmt.Scanf("%d%*c", &idx)
			var s Data = &MyStr{idx: idx}
			s.init(nil)
		case 2:
			fmt.Scanf("%d%*c", &idx)
			l.info(idx)
		case 3:
			fmt.Scanf("%d%*c", &idx)
			l.edit(idx)
		}
	}
}
