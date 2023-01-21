#  Copyright 2023 Mahid
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY
import pygame,sys,textwrap
from pygame.locals import*
import glob
import time
import pickle
import os
pygame.init()

path = os.path.expanduser('~\Documents\\01one\Time True\TaskData.pickle')


try:
	with open(path, 'rb') as data:
		all_data= pickle.load(data)
		data.close()
except:
	task_data=os.path.expanduser('~\Documents\\01one\Time True')
	if not os.path.exists(task_data):
		os.makedirs(task_data)
	with open(path, 'wb') as data:
		all_data=[]
		note_txt=''
		task_l=[[],[],[],[],[]]
		all_data.append(note_txt)
		all_data.append(task_l)
		pickle.dump(task_l, data)
		data.close()

wrapper = textwrap.TextWrapper(fix_sentence_endings=True,width=28)

graphics=glob.glob("data/*.png")
graphics_list=[]
for item in graphics:
	data=pygame.image.load(item)
	graphics_list.append(data)
background=graphics_list[0]
task=graphics_list[1]
add=graphics_list[2]
remove=graphics_list[3]
edit=graphics_list[4]
icon=graphics_list[5]

clock=pygame.time.Clock()
screen=pygame.display.set_mode((1280,720))
pygame.display.set_icon(icon)
pygame.display.set_caption("Time True")
color=(144, 238,144)






font=pygame.font.Font('data/PlayfairDisplay-Bold.ttf',24)

current_c=0
current_i=0

edit_number=0
edit1=False
pulse=''
task_l=all_data[1]
note_txt=all_data[0]
note_edit=False
note=pygame.Rect(840,80,390,600)
total_line=0

note_font=pygame.font.Font('data/DidactGothic-Regular.ttf',24)

class TextEdit():
	def __init__(self,screen,text='',t_x=0,t_y=0,t_w=200,t_h=400,text_color="#F0F8FF",font=note_font):
		self.screen=screen
		self.t_x=t_x
		self.t_y=t_y
		self.t_w=t_w
		self.t_h=t_h
		self.text_color=text_color
		self.text_font=font
		self.text_lines=[]
		
		self.text_lines=wrapper.wrap(text=text)
		
		text_row=self.t_y
		global total_line
		total_line=len(self.text_lines)

		for line in self.text_lines:
			if line != "":
				text_surface = self.text_font.render(line, 1, self.text_color)
				text_surface.set_alpha(75)
				self.screen.blit(text_surface, (self.t_x, self.t_y))
			self.t_y +=self.text_font.size(line)[1]


class TextView():
	def __init__(self,screen,text='',t_x=0,t_y=0,t_w=167,text_color="#666666",font=font):
		self.screen=screen
		self.t_x=t_x
		self.t_y=t_y
		self.t_w=t_w
		self.text_color=text_color
		self.task_txt=text
		self.text_font=font
		text_surface = self.text_font.render(self.task_txt, 1, self.text_color)
		text_surface.set_alpha(75)
		self.screen.blit(text_surface, (self.t_x, self.t_y))


class Quadrant():
	global taskt_l
	def __init__(self,surface=screen,x=0,y=0,c=0):
		self.x=x
		self.y=y
		self.d=66
		self.c=c
		self.surface=surface
		self.mouse_position=pygame.mouse.get_pos()
		self.task_list=task_l[self.c]
		self.n=len(self.task_list)


		self.c_r=pygame.Rect(self.x+16,self.y+35,261,261)
		self.add_rect=pygame.Rect(self.x+123,self.y+66*self.n+41,44,44)
		self.task_rect=[]
		self.remove_rect=[]
		self.edit_rect=[]
		d_r=False
		
		
		for i in range(self.n):
			r=pygame.Rect(self.x+37,self.y+66*i+35,217,55)
			self.task_rect.append(r)
			r1=pygame.Rect(self.x+206,self.y+66*i+41,44,44)
			self.remove_rect.append(r1)
			r2=pygame.Rect(self.x+40,self.y+66*i+40,21,30)
			self.edit_rect.append(r2)

		global edit1,current_c,current_i,note_edit
		
		
		remove_task=False
		for i in range(self.n):
			self.surface.blit(task,(self.x,self.y+self.d*i))
			TextView(self.surface,text=self.task_list[i],t_x=self.x+64,t_y=self.y+66*i+45,t_w=167,text_color="#ffe6f3",font=font)
		if self.n<4:
			self.surface.blit(add,(self.x+87,self.y+self.d*self.n+5))
		if self.c_r.collidepoint(self.mouse_position):
			for i in range(self.n):
				if self.task_rect[i].collidepoint(self.mouse_position):
					self.surface.blit(remove,(self.x+164,self.y+i*self.d+22))
					self.surface.blit(edit,(self.x+40,self.y+i*self.d+40))

					if event.type==pygame.MOUSEBUTTONDOWN:
						if event.button==1:
							if self.remove_rect[i].collidepoint(self.mouse_position):
								remove_task=True
								current_c=self.c
								current_i=i
							elif self.edit_rect[i].collidepoint(self.mouse_position):
								edit1=True
								note_edit=False
								current_i=i
								current_c=self.c

				
			if event.type==pygame.MOUSEBUTTONDOWN:
				if event.button==1:
					if remove_task:
						del task_l[self.c][current_i]
						time.sleep(.1)
						remove_task=False
					if self.n<4:
						if self.add_rect.collidepoint(self.mouse_position):
							task_l[self.c].append('task')
							time.sleep(.01)
		


game_running=True
while game_running:
	clock.tick(60)
	mouse_position=pygame.mouse.get_pos()
	for event in [pygame.event.wait()]+pygame.event.get():
	#for event in pygame.event.get():
		if event.type==QUIT:
			with open(path, 'wb') as data:
				all_data=[]
				all_data.append(note_txt)
				all_data.append(task_l)
				pickle.dump(all_data, data)
				data.close()
			pygame.quit()
			sys.exit()
		

	
		if note.collidepoint(mouse_position):
			if event.type==pygame.MOUSEBUTTONDOWN:
				note_edit=True
				edit1=False
			
		if event.type==pygame.TEXTINPUT:
			if edit1:
				if len(task_l[current_c][current_i])<14:
					task_l[current_c][current_i]+=event.text
			if total_line<18 and  note_edit:
				note_txt+=event.text
				
	
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_BACKSPACE:
				pygame.key.set_repeat(200,5)
				if edit1:
					if len(task_l[current_c][current_i])>0:
						task_l[current_c][current_i]=task_l[current_c][current_i][:-1]
				if note_edit:
					if len(note_txt)>0:
						note_txt=note_txt[:-1]
						
		

	screen.blit(background,(0,0))
	
	Quadrant(x=140,y=91,c=0)
	Quadrant(x=430,y=91,c=1)
	Quadrant(x=140,y=386,c=2)
	Quadrant(x=430,y=386,c=3)
	TextEdit(screen,text=note_txt,t_x=860,t_y=110,t_w=340,t_h=530)
	pygame.display.update()
