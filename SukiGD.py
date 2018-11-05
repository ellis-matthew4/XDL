import os

TOKEN_POSITIONS = "POSITIONS:"
TOKEN_POS = "Position"
TOKEN_CHARACTERS = "CHARACTERS:"
TOKEN_CHAR = "Character"
TOKEN_EMOTION = "Emotion"
TOKEN_SHOW = "show"
TOKEN_HIDE = "hide"

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
			temp = { }
		elif statement[0] == TOKEN_POS:
			vec = statement[3].strip("()")
			pivot = vec.index(",")
			x = vec[:pivot]
			y = vec[pivot+1:]
			temp[statement[1]] = {"x": x, "y": y}
		elif statement[0] == TOKEN_CHARACTERS:
			out["Positions"] = temp
			temp = { }
		elif statement[0] == TOKEN_CHAR:
			if temp != { }:
				out[currentCharName] = temp
				temp = { }
				EM_INDEX = 0
			currentCharName = statement[1]
			temp["path"] = statement[3]
		elif statement[0] == TOKEN_EMOTION:
			temp[statement[1]] = EM_INDEX
			EM_INDEX += 1
		else:
			if temp != { }:
				temp = { }
			if statement[0] == TOKEN_SHOW:
				temp["action"] = statement[0]
				temp["char"] = statement[1]
				temp["emote"] = statement[2]
				if statement[3] == "at":
					temp["pos"] = statement[4]
				else:
					temp["pos"] = statement[3]
			elif statement[0] == TOKEN_HIDE:
				temp["action"] = statement[0]
				temp["char"] = statement[1]
			else:
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