
import sys

class TestOne(object):
	def run(self):
		print("Test One")
	def process(self):
		try:
		    print("Press CTRL-C to stop")
		    self.run()
		except KeyboardInterrupt:
		    print("Exiting\n")
		    sys.exit(0)

class TestTwo(TestOne):
	def run(self):
		print("Test Two")

Tester = TestTwo()
while True:
    Tester.process()