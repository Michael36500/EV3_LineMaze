import time
#!/usr/bin/env pybricks-micropython

# Function for nth Fibonacci number
def Fibonacci(n):

	# Check if input is 0 then it will
	# print incorrect input
	if n < 0:
		print("Incorrect input")

	# Check if n is 0
	# then it will return 0
	elif n == 0:
		return 0

	# Check if n is 1,2
	# it will return 1
	elif n == 1 or n == 2:
		return 1

	else:
		return Fibonacci(n-1) + Fibonacci(n-2)
    
t1 = time.time()
# Driver Program
for x in range(30):
    print(Fibonacci(x), x)
t2 = time.time()
print(t2 - t1)

# This code is contributed by Saket Modi
# then corrected and improved by Himanshu Kanojiya



# ev3 93.8058919907
# my pc 0.29107046127319336