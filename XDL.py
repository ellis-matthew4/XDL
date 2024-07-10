import os
import json

TOKEN_SHOW = "show"
TOKEN_HIDE = "hide"
TOKEN_EQ = "="
TOKEN_SCENE = "scene"
TOKEN_LABEL = "label"
TOKEN_RETURN = "return"
TOKEN_SEMICOLON = ":"
TOKEN_CALL = "call"
TOKEN_JUMP = "jump"
TOKEN_VAR = "var"
TOKEN_MENU = "menu:"
TOKEN_OPTION = "option"
TOKEN_ACTION = "action"
TOKEN_WINDOW = "window"
TOKEN_PLAY = "play"
TOKEN_CENTERED = "centered"
TOKEN_IF = "if"
TOKEN_INCLUDE = "include"

STMT_SHOW = 5
STMT_HIDE = 6
STMT_DIALOG = 7
STMT_SCENE = 10
STMT_LABEL = 11
STMT_RETURN = 12
STMT_CALL = 13
STMT_JUMP = 14
STMT_VAR = 15
STMT_MENU = 16
STMT_OPTION = 17
STMT_END = 18
STMT_ACTION = 19
STMT_WINDOW = 20
STMT_PLAY = 21
STMT_IF = 22
STMT_INCLUDE = 23

LEN_SHOW = [4, 5]
LEN_HIDE = 2
LEN_DIALOG = [2, 3]
LEN_SCENE = 2
LEN_LABEL = 2
LEN_RETURN = 1
LEN_CALL = 2
LEN_JUMP = 2
LEN_VAR = 4
LEN_MENU = 1
LEN_OPTION = 4
LEN_WINDOW = 2
LEN_PLAY = 2
LEN_IF = 6
LEN_INCLUDE = 2

OPERATORS = ['==','<=','>=','!=','>','<']

operator = -10
operand = -20
leftparentheses = -30
rightparentheses = -40
empty = -50

SYNTAXERROR = "Syntax error on the above line."
TOKENERROR = "Syntax Error: The number of tokens on the above line is illegal."
STRINGERROR = "Syntax Error: Tried to set a name literal to a string."

def reStitch(STMT):
	s = ""
	for k in STMT:
		s += str(k) + " "
	return s

def checkSyntax(TYPE, STMT):
	if TYPE == STMT_SHOW:
		if len(STMT) not in LEN_SHOW:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		elif isString(STMT[1]) or isString(STMT[2]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Strings are not accepted in Show statements.")
		else:
			if len(STMT) == 4:
				if isString(STMT[3]):
					print(reStitch(STMT))
					raise Exception("Syntax Error: Strings are not accepted in Show statements.")
			else:
				if isString(STMT[4]):
					print(reStitch(STMT))
					raise Exception("Syntax Error: Strings are not accepted in Show statements.")
				elif STMT[3] != "at":
					print(reStitch(STMT))
					raise Exception("Syntax Error: Token 3: Expected 'at', got " + STMT[3])
	elif TYPE == STMT_HIDE:
		if len(STMT) != LEN_HIDE:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		elif isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception(STRINGERROR)
	elif TYPE == STMT_DIALOG:
		if len(STMT) not in LEN_DIALOG:
			print(str(STMT))
			raise Exception(TOKENERROR)
		elif len(STMT) == 2:
			if not isString(STMT[1]):
				print(reStitch(STMT))
				raise Exception("String expected, got " + STMT[1])
		elif len(STMT) == 3:
			if isString(STMT[1]):
				print(reStitch(STMT))
				raise Exception(STRINGERROR)
			elif not isString(STMT[2]):
				print(reStitch(STMT))
				raise Exception("String expected, got " + STMT[2])
	elif TYPE == STMT_SCENE:
		if len(STMT) != LEN_SCENE:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		elif isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 1: Unexpected String.")
	elif TYPE == STMT_LABEL:
		if len(STMT) != LEN_LABEL:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		elif isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 1: Unexpected String.")
	elif TYPE == STMT_RETURN:
		if len(STMT) != LEN_RETURN:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
	elif TYPE == STMT_CALL:
		if len(STMT) != LEN_CALL:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		elif isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 1: Unexpected String.")
	elif TYPE == STMT_JUMP:
		if len(STMT) != LEN_JUMP:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		elif isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 1: Unexpected String.")
	elif TYPE == STMT_VAR:
		if len(STMT) != LEN_VAR:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		elif isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 1: Unexpected String.")
		elif STMT[2] != TOKEN_EQ:
			print(reStitch(STMT))
			raise Exception(SYNTAXERROR)
	elif TYPE == STMT_MENU:
		if len(STMT) != LEN_MENU:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
	elif TYPE == STMT_OPTION:
		if len(STMT) != LEN_OPTION:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		if not isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 1: Expected String.")
		if STMT[2] not in [ TOKEN_CALL, TOKEN_JUMP ]:
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 2: Invalid protocol.")
		if isString(STMT[3]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 3: Unexpected String.")
	elif TYPE == STMT_ACTION:
		if len(STMT) < 2:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		if isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 1: Unexpected String.")
	elif TYPE == STMT_WINDOW:
		if len(STMT) != LEN_WINDOW:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		if STMT[1] not in [TOKEN_SHOW, TOKEN_HIDE]:
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 2 can only be show or hide.")
	elif TYPE == STMT_PLAY:
		if len(STMT) != LEN_PLAY:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		if isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 1: Unexpected String.")
	elif TYPE == STMT_IF:
		if len(STMT) != LEN_IF:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		if STMT[4] not in [TOKEN_CALL,TOKEN_JUMP]:
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 4: Unknown protocol " + STMT[4] + ".")
		if isString(STMT[5]):
			print(reStitch(STMT))
			raise Exception("Syntax Error: Token 5: Unexpected String.")
	elif TYPE == STMT_INCLUDE:
		if len(STMT) != LEN_HIDE:
			print(reStitch(STMT))
			raise Exception(TOKENERROR)
		elif not isString(STMT[1]):
			print(reStitch(STMT))
			raise Exception("String expected, got " + STMT[1])
	else:
		print(reStitch(STMT))
		raise Exception("I don't know what you did, but don't do it again.")
		

def isString(s): #Checks to see if the token is of type TOKEN_STRING
	if s == '':
		return False
	return s[0] == s[-1] and s[0] == '"'

def parse(filename): #Takes the list of tokens created by the scan function and turns them into a dictionary
	statements = scan('input/' + filename)
	out = { }
	labels = { }
	temp = { }
	bg = { }
	menu = { "action":"menu" }
	currentLabel = ""
	dialogue = []
	for statement in statements:
		if statement[0] == TOKEN_LABEL:
			checkSyntax(STMT_LABEL, statement)
			currentLabel = statement[1][0:]
		elif statement[0] == TOKEN_INCLUDE:
			print("Performing an inclusion parse of "+statement[1])
			k = parse(statement[1][1:])
			for key in k["labels"].keys():
				labels[key] = k["labels"][key]
		elif statement[0] == TOKEN_OPTION:
			if menu != { "action" : "menu" }:
				temp = { }
				checkSyntax(STMT_OPTION, statement)
				temp["action"] = statement[0]
				temp["string"] = statement[1]
				temp["protocol"] = statement[2]
				temp["target"] = statement[3]
				menu["options"].append(temp)
				temp = { }
			else:
				raise Exception("Bad menu block")
		elif menu != { "action":"menu" }: # Exit condition for menu options
			dialogue.append(menu)
			menu = { "action":"menu" }
		elif statement[0] == TOKEN_MENU:
			menu["options"] = []
		elif statement[0] == TOKEN_RETURN:
			checkSyntax(STMT_RETURN, statement)
			labels[currentLabel] = dialogue
			dialogue = []
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
			elif statement[0] == TOKEN_SCENE:
				checkSyntax(STMT_SCENE, statement)
				temp["action"] = statement[0]
				temp["scene"] = statement[1]
			elif statement[0] == TOKEN_CALL:
				checkSyntax(STMT_CALL, statement)
				temp["action"] = statement[0]
				temp["label"] = statement[1]
			elif statement[0] == TOKEN_JUMP:
				checkSyntax(STMT_JUMP, statement)
				temp["action"] = statement[0]
				temp["label"] = statement[1]
			elif statement[0] == TOKEN_VAR:
				checkSyntax(STMT_VAR, statement)
				temp["action"] = statement[0]
				temp["name"] = statement[1]
				if statement[3] == "true" or statement[3] == "false":
					temp["value"] = eval(statement[3].capitalize())
				else:
					temp["value"] = eval(statement[3])
			elif statement[0] == TOKEN_ACTION:
				checkSyntax(STMT_ACTION, statement)
				temp["action"] = statement[1]
				if len(statement) > 2:
					temp["args"] = statement[2:]
			elif statement[0] == TOKEN_WINDOW:
				checkSyntax(STMT_WINDOW, statement)
				temp["action"] = statement[0]
				temp["value"] = statement[1]
			elif statement[0] == TOKEN_PLAY:
				checkSyntax(STMT_PLAY, statement)
				temp["action"] = statement[0]
				temp["anim"] = statement[1]
			elif statement[0] == TOKEN_CENTERED:
				checkSyntax(STMT_DIALOG, statement)
				if isString(statement[1]):
					temp["action"] = "centered"
					temp["char"] = statement[0]
					temp["String"] = statement[1]
			elif statement[0] == TOKEN_IF:
				statement = createCondition(statement)
				checkSyntax(STMT_IF, statement)
				temp["action"] = statement[0]
				temp["op1"] = statement[1]
				temp["opr"] = statement[2]
				temp["op2"] = statement[3]
				temp["protocol"] = statement[4]
				temp["target"] = statement[5]
			else:
				if isString(statement[0]):
					temp["action"] = "adialogue"
					temp["String"] = statement[0]
				else:
					checkSyntax(STMT_DIALOG, statement)
					if isString(statement[1]):
						temp["action"] = "dialogue"
						temp["char"] = statement[0]
						temp["String"] = statement[1]
					else:
						temp["action"] = "dialogue"
						temp["char"] = statement[0]
						temp["emote"] = statement[1]
						temp["String"] = statement[2]
			dialogue.append(temp)
	if bg != { }:
		out["Backdrops"] = bg
	if labels != { }:
		out["labels"] = labels
	return out

def createCondition(s):
	new = []
	token = []
	for t in s:
		if t in OPERATORS:
			pivot = s.index(t)
		if t == TOKEN_CALL or t == TOKEN_JUMP:
			endpoint = s.index(t)
			break
	new.append(s[0])
	for t in s[1:pivot]:
		token.append(t)
	new.append(convert(token))
	new.append(s[pivot])
	token = []
	for t in s[pivot+1:endpoint]:
		token.append(t)
	new.append(convert(token))
	new.append(s[endpoint])
	new.append(s[endpoint+1])
	return new
	
def precedence(s): # From https://ragsagar.wordpress.com/2009/09/22/infix-to-postfix-conversion-in-python/
    if s == '(':
        return 0
    elif s == '+' or s == '-':
        return 1
    elif s == '*' or s == '/' or s == '%':
        return 2
    else:
        return 99
                 
def typeof(s): # From https://ragsagar.wordpress.com/2009/09/22/infix-to-postfix-conversion-in-python/
    if s == '(':
        return leftparentheses
    elif s == ')':
        return rightparentheses
    elif s == '+' or s == '-' or s == '*' or s == '%' or s == '/':
        return operator
    elif s == ' ':
        return empty    
    else :
        return operand                          
 
def convert(infix): # From https://ragsagar.wordpress.com/2009/09/22/infix-to-postfix-conversion-in-python/
	postfix = []
	temp = []
	for i in infix :
		char_type = typeof(i)
		if char_type == leftparentheses :
			temp.append(i)
		elif char_type == rightparentheses :
			next_char = temp.pop()
			while next_char != '(':
				postfix.append(next_char)
				next_char = temp.pop()
		elif char_type == operand:
			postfix.append(i)
		elif char_type == operator:
			p = precedence(i)
			while len(temp) != 0 and p <= precedence(temp[-1]) :
				postfix.append(temp.pop())
			temp.append(i)
		elif char_type == empty:
			continue
					 
	while len(temp) > 0 :
		postfix.append(temp.pop())
	return postfix

def scanLine(line):
	if line.strip() == "" or line[0] == "#":
		return []
	l = []
	word = ""
	string = False
	for c in line:
		if c == "\t":
			continue
		if not string:
			if c == " " or c == "\n" or c == "\r" or c == "":
				if word == '':
					continue
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
	return l

def scan(filename): #Turns the input file into a list of lines, and each line into a list of tokens
	f = open(filename, "r")
	lines = []
	for line in f.readlines():
		l = scanLine(line)
		if l == []:
			continue
		lines.append(l)
	return lines

for filename in os.listdir('input/'): #Parses all input files, and writes their dictionaries to JSON files in the output folder
	print("Now scanning " + filename + "...")
	k = parse(filename)
	filename = filename.rstrip(".txt")
	filename = "output/" + filename + ".json"
	with open(filename, "w") as f:
		json.dump(k,f)
	f.close()
print("Done!")
