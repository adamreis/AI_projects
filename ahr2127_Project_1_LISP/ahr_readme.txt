Adam Reis
ahr2127
Artificial Intelligence
Assignment 1 -- Pattern matching in LISP

Programming language: LISP

Version: Whatever is standard in OSX Mountain Lion

Development Environment: I used Sublime Text as my text editor and ran
						 everything in LispWorks Personal on OSX Mountain Lion

Running it in LispWorks: File -> 'Compile and Load' -> ahr2127.lisp 
						 -> (match '(pattern) '(data))

How it works: The user calls 'match', which itself calls a helper function
			'rpm' which includes an extra argument for storing an association
			list.  From there, the comments in my code outline the structure
			of how things work (essentially a bunch of cond statements that
			define the program's behavior based on (first p)).
