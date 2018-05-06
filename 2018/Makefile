INPUT ?= ./file_1MB.txt
OUTPUT ?= ./output.txt


test:
	python2 receiver.py > $(OUTPUT) & time python2 sender.py < $(INPUT) &
diff:
	diff $(INPUT) $(OUTPUT)
kill:
	pkill python2
clean:
	rm *.log $(OUTPUT) *.pyc
