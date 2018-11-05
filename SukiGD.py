import os

TOKEN_POSITIONS = "POSITIONS:"
TOKEN_POS = "Position"
TOKEN_CHARACTERS = "CHARACTERS:"
TOKEN_CHAR = "Character"
TOKEN_EMOTION = "Emotion"
TOKEN_SHOW = "show"
TOKEN_HIDE = "hide"
TOKEN_EQ = "="

STMT_POSITIONS = 0
STMT_POS = 1
STMT_CHARACTERS = 2
STMT_CHAR = 3
STMT_EMOTION = 4
STMT_SHOW = 5
STMT_HIDE = 6
STMT_DIALOG = 7

LEN_POSITIONS = 1
LEN_POS = 4
LEN_CHARACTERS = 1
LEN_CHAR = 4
LEN_EMOTION = 2
LEN_SHOW = [4, 5]
LEN_HIDE = 2
LEN_DIALOG = [2, 3]

SYNTAXERROR = "Syntax error on the above line."
TOKENERROR = "Syntax Error: The number of tokens on the above line is illegal."
STRINGERROR = "Syntax Error: Tried to set a name literal to a string."
FINALSTRINGERROR = "Syntax Error: Final argument should be a String containing a path to a Node."
FINALVECERROR = "Syntax Error: Final argument should be a 2D Vector. Example: (0.0,0.0)"

def checkSyntax(TYPE, STMT):
	if TYPE == STMT_POSITIONS:
		if len(STMT) != LEN_POSITIONS:
			print(STMT)
			raise Exception(SYNTAXERROR)
	elif TYPE == STMT_POS or TYPE == STMT_CHAR:
		if len(STMT) > LEN_POS or len(STMT) < LEN_POS:
			print(STMT)
			raise Exception(TOKENERROR)
		else:
			if STMT[2] != TOKEN_EQ:
				print(STMT)
				raise Exception(SYNTAXERROR)
			elif isString(STMT[1]):
				print(STMT)
				raise Exception(STRINGERROR)
			elif TYPE == STMT_CHAR and not isString(STMT[3]):
				print(STMT)
				raise Exception(FINALSTRINGERROR)
			elif TYPE == STMT_POS:
				k = STMT[3]
				if k[0] != "(" or k[-1] != ")":
					raise Exception(FINALVECERROR)
	elif TYPE == STMT_CHARACTERS:
		if len(STMT) != LEN_CHARACTERS:
			print(STMT)
			raise Exception(SYNTAXERROR)
	elif TYPE == STMT_EMOTION:
		if len(STMT) != LEN_EMOTION:
			print(STMT)
			raise Exception(TOKENERROR)
		elif isString(STMT[1]):
			print(STMT)
			raise Exception(STRINGERROR)
	elif TYPE == STMT_SHOW:
		if not len(STMT) in LEN_SHOW:
			print(STMT)
			raise Exception(TOKENERROR)
		elif isString(STMT[1]) or isString(STMT[2]):
			print(STMT)
			raise Exception("Syntax Error: Strings are not accepted in Show statements.")
		else:
			if len(STMT) == 4:
				if isString(STMT[3]):
					print(STMT)
					raise Exception("Syntax Error: Strings are not accepted in Show statements.")
			else:
				if isString(STMT[4]):
					print(STMT)
					raise Exception("Syntax Error: Strings are not accepted in Show statements.")
				elif STMT[3] != "at":
					print(STMT)
					raise Exception("Syntax Error: Token 3: Expected 'at', got " + STMT[3])
	elif TYPE == STMT_HIDE:
		if len(STMT) != LEN_HIDE:
			print(STMT)
			raise Exception(TOKENERROR)
		elif isString(STMT[1]):
			print(STMT)
			raise Exception(STRINGERROR)
	elif TYPE == STMT_DIALOG:
		if not len(STMT) in LEN_DIALOG:
			print(STMT)
			raise Exception(TOKENERROR)
		elif len(STMT) == 2:
			if not isString(STMT[1]):
				print(STMT)
				raise Exception("String expected, got " + STMT[1])
		elif len(STMT) == 3:
			if isString(STMT[1]):
				print(STMT)
				raise Exception(STRINGERROR)
			elif not isString(STMT[2]):
				raise Exception("String expected, got " + STMT[2])
	else:
		print(STMT)
		raise Exception("I don't know what you did, but don't do it again.")
		

def isString(s): #Checks to see if the token is of type TOKEN_STRING
	return s[0] == s[-1] and s[0] == '"'

def parse(filename): #Takes the list of tokens created by the scan function and turns them into a dictionary
	statements = scan('input/' + filename)
	out = { }
	temp = { }
	currentCharName = ""
	EM_INDEX = 0
	dialogue = []
	for statement in statements:
		if statement[0] == TOKEN_POSITIONS:
			checkSyntax(STMT_POSITIONS, statement)
			temp = { }
		elif statement[0] == TOKEN_POS:
			checkSyntax(STMT_POS, statement)
			vec = statement[3].strip("()")
			pivot = vec.index(",")
			x = vec[:pivot]
			y = vec[pivot+1:]
			temp[statement[1]] = {"x": x, "y": y}
		elif statement[0] == TOKEN_CHARACTERS:
			checkSyntax(STMT_CHARACTERS, statement)
			out["Positions"] = temp
			temp = { }
		elif statement[0] == TOKEN_CHAR:
			checkSyntax(STMT_CHAR, statement)
			if temp != { }:
				out[currentCharName] = temp
				temp = { }
				EM_INDEX = 0
			currentCharName = statement[1]
			temp["path"] = statement[3]
		elif statement[0] == TOKEN_EMOTION:
			checkSyntax(STMT_EMOTION, statement)
			temp[statement[1]] = EM_INDEX
			EM_INDEX += 1
		else:
			if temp != { }:
				temp = { }
			if statement[0] == TOKEN_SHOW:
				checkSyntax(STMT_SHOW, statement)
				temp["action"] = statement[0]
				temp["char"] = statement[1]
				temp["emote"] = statement[2]
				if statement[3] == "at":
					temp["pos"] = statement[4]
				else:
					temp["pos"] = statement[3]
			elif statement[0] == TOKEN_HIDE:
				checkSyntax(STMT_HIDE, statement)
				temp["action"] = statement[0]
				temp["char"] = statement[1]
			else:
				checkSyntax(STMT_DIALOG, statement)
				if isString(statement[1]):
					temp["char"] = statement[0]
					temp["String"] = statement[1]
				else:
					temp["char"] = statement[0]
					temp["emote"] = statement[1]
					temp["String"] = statement[2]
			dialogue.append(temp)
	if dialogue == []:
		return out
	else:
		return dialogue

def scan(filename): #Turns the input file into a list of lines, and each line into a list of tokens
	f = open(filename, "r")
	lines = []
	lineNum = 0
	string = False
	for line in f.readlines():
		l = []
		word = ""
		for c in line:
			if not string:
				if c == " " or c == "\n":
					l.append(word)
					word = ""
				elif c == '"':
					word += c
					string = True
				else:
					word += c
			else:
				if c != '"':
					word += c
				else:
					word += c
					string = False
		if word != "":
			l.append(word)
		lines.append(l)
	return lines

for filename in os.listdir('input/'): #Parses all input files, and writes their dictionaries to JSON files in the output folder
	print("Now scanning " + filename + "...")
	k = parse(filename)
	filename = filename.rstrip(".txt")
	filename = "output/" + filename + ".json"
	f = open(filename, "w")
	f.write(str(k))
	f.close()
print("Done!")