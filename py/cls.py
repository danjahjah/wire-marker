from PIL import Image, ImageDraw


class Dot(object):

	coord_1={
		0:(None),
		1:(0,0),
		2:(0,1),
		3:(0,2),
		4:(1,2),
		5:(1,1),
		6:(1,0)

	}

	coord_0={
		0:(None),
		1:(0,2),
		2:(0,1),
		3:(0,0),
		4:(1,0),
		5:(1,1),
		6:(1,2)

	}
	coord = coord_1


class Glyph(object):
	"""docstring for Glyph"""
	LINE_DELIMETER=';'
	LETTER_SPACING = 0.5

	lst={}

	def __init__(self, name, seq,pos=0,fs=1, reverse=True ):
		super(Glyph, self).__init__()
		self.name = name
		self.seq = seq.split(Glyph.LINE_DELIMETER)
		self.reverse=reverse
		self.lines=list()
		self.coords=list()
		self.position=pos

		self.font_size= fs

		self.start_pos()
		self.seq_to_lines()
		self.lines_to_coords()

		Glyph.lst[self.name]=self


	def start_pos(self):
		is_first = int(self.position>0)
		self.sp = self.position*self.font_size + self.position*Glyph.LETTER_SPACING*self.font_size*is_first
		

	def seq_to_line(sel, seq):
		line=list()
		for i in seq:
			if i==Glyph.LINE_DELIMETER: break
			line.append(Dot.coord[int(i)])

		return line


	def seq_to_lines(self):
		
		for s in self.seq:
			self.lines.append(self.seq_to_line(s))

		# print(self.lines)

	def line_to_coord(self, l):
		coords=list()
		for p in l:
			x= p[0]*self.font_size+self.sp
			y= p[1]*self.font_size

			coords.append((x,y))

		return coords
		

	def lines_to_coords(self):
		
		self.coords.clear()
		self.start_pos()

		for l in self.lines:
			self.coords.append(self.line_to_coord(l))


	def gcode_coords_diff(self, p0, p1):
		dx = p1[0]-p0[0]
		dy = p1[1]-p0[1]

		x = f" X{dx}" if dx!=0 else ""
		y = f" Y{dy}" if dy!=0 else ""

		return f"{x}{y}"


	def line_to_gcode(self,l, c, bySymbol=False):	

		
		if not l:
			return

		glines=["M5"]
		# начинаем в абсолютных координатах
		if bySymbol==True:
			glines.append(f"G90 X{l[0][0]} Y{l[0][1]}")
		else:
			glines.append(f"G90 X{c[0][0]} Y{c[0][1]}")

		glines.append("M3")
		glines.append("G91 F100")

		# символ в относительных
		for prev, lc in zip(l,l[1:]):
			glines.append(f"G1{self.gcode_coords_diff(prev,lc)}")
			# glines.append(f"G1 X{lc[0]} Y{lc[1]}")

		return glines

	def lines_to_gcode(self):
		glines=[f"\n;Symbol <{self.name}>"]
		# print(f"\n;Symbol <{self.name}>")

		if not self.lines[0]:
			glines.append(f";Symbol <{self.name}>skip")
			# print(f";Symbol <{self.name}>skip")	
			return


		for l,c in zip(self.lines,self.coords):
			glines.extend(self.line_to_gcode(l,c))

		# for s in glines:
		# 	print(s)
		return glines


class Word(object):
	"""docstring for Word"""
	def __init__(self, text, fs=40):		
		self.text = text
	
	def print_text(self):
		w = len(self.text)*60
		img = Image.new("RGB", (w, 90), color="green")
		img1 = ImageDraw.Draw(img) 

		for idx,l in enumerate(self.text):
			g = Glyph.lst.get(l)
			g.position=idx
			g.lines_to_coords()
			for l in  g.coords:
				img1.line(l,  width = 0)

			
		img.show()

	def get_gcode(self):
		glines = [f";Start text <{self.text}>"]
		# print(f";Start text <{self.text}>")
		for idx,l in enumerate(self.text):
			g = Glyph.lst.get(l)
			g.position=idx
			g.lines_to_coords()
			g_string = g.lines_to_gcode()
			if g_string:
				glines.extend(g_string)
			# for l in  g.coords:
			# 	img1.line(l,  width = 0)
		glines.append(f";=== End of text <{self.text}> ===\n")
		# print(f";End\n")
		return glines



	
		
def init_glyphs():
	
	gl_x = Glyph('X', '14;36')
	gl_k = Glyph('K', '13;624')
	gl_r = Glyph('R', '13;62543')
	gl_z = Glyph('Z', '6143')
	gl_a = Glyph('A', '1246;25')
	gl_space = Glyph(' ', '')
	gl_Line = Glyph('-', '25')

	gl_0 = Glyph('0', '13461')
	gl_1 = Glyph('1', '246')
	gl_2 = Glyph('2', '34516')
	gl_3 = Glyph('3', '34251')
	gl_4 = Glyph('4', '325;46')
	gl_5 = Glyph('5', '165234')
	gl_6 = Glyph('6', '421652')
	gl_7 = Glyph('7', '1243')
	gl_8 = Glyph('8', '13461;25')
	gl_9 = Glyph('9', '154325')

	








#--------------
init_glyphs()

t = Word("X12-3456789 KRZA")

s = t.get_gcode()

print('\n'.join(s))

with open('readme.nc', 'w') as f:
    f.write('\n'.join(s))


