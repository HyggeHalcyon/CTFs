obj-m += vuln.o
vuln-objs := chal.o

clean:
	rm -f ./chal.o ./vuln.o ./vuln.ko
	rm -f ./.vuln.o.cmd ./.vuln.mod.o.cmd ./.vuln.mod.cmd ./.vuln.ko.cmd ./.chal.o.cmd
	rm -f ./.Module.symvers.cmd ./.modules.order.cmd
	rm -f ./vuln.mod ./Module.symvers ./modules.order
	rm -f ./vuln.mod ./vuln.mod.c ./vuln.mod.o
