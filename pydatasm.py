def token_datasm(s):
	z = []
	incom = False
	instr = False
	for i in s:
		if i == " " or i == ",":
			if not instr and not incom:
				z.append("")
			elif not incom:
				z[-1] += i

		elif i == "\n":
			z.append(";")
			z.append("")
			incom = False
			instr = False

		elif i == "\"":
			if not incom:
				z[-1] += "\""
				instr = not instr

		elif i == ";":
			incom = True

		elif i == "\t":
			if not incom and instr:
				z[-1] += "\t"

		else:
			if not incom:
				z[-1] += i

	while "" in z:
		z.remove("")

	return z

def datasm(s):
	x = token_datasm(s)
	i = 0
	lab = None
	sublab = None
	dat = {}
	while i < len(x):
		e = x[i]
		if e == ";":
			pass
		elif e[0] == ".":
			sublab = e[1:-1]
			if lab not in dat:
				dat[lab] = {}
			if sublab not in dat[lab]:
				dat[lab][sublab] = ""

		elif e[-1] == ":":
			lab = e[:-1]
			sublab = None
			if lab not in dat:
				dat[lab] = {}

		elif e == "db":
			if lab not in dat:
				dat[lab] = {}
			if sublab not in dat[lab]:
				dat[lab][sublab] = ""
			if x[i-1] == ";":
				f = ""
				while True:
					i += 1
					if x[i] != ";":
						if x[i][0] == "\"":
							f += x[i][1:-1]

						elif x[i].startswith("0x"):
							f += chr(int(x[i][2:], 16))

						elif x[i].startswith("0b"):
							f += chr(int(x[i][2:], 2))

						elif x[i].startswith("0") and len(x[i]) > 1:
							f += chr(int(x[i][1:], 8))

						else:
							f += chr(int(x[i], 10))

					if x[i] == ";":
						break
				dat[lab][sublab] += f

		elif e == "dw":
			if lab not in dat:
				dat[lab] = {}
			if sublab not in dat[lab]:
				dat[lab][sublab] = ""
			if x[i-1] == ";":
				f = ""
				while True:
					i += 1
					if x[i] != ";":
						e = 0
						if x[i].startswith("0x"):
							e = int(x[i][2:], 16)

						elif x[i].startswith("0b"):
							e = int(x[i][2:], 2)

						elif x[i].startswith("0") and len(x[i]) > 1:
							e = int(x[i][1:], 8)

						else:
							e = int(x[i], 10)

						e1 = chr(e & 0x00FF)
						e2 = chr(e & 0xFF00)
						f += e2
						f += e1

					if x[i] == ";":
						break

				dat[lab][sublab] += f

		i += 1

	return dat

def loaddatasm(filename):
	with open(filename) as f:
		return datasm(f.read())

def loadsdatasm(file):
	return datasm(file.read())
