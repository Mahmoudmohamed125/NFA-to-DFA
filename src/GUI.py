import pygame
import pygame_textinput
from pygame_textinput import TextInputManager, TextInputVisualizer #take input from the user
import math
from graphviz import Digraph
import io
import time
import NFA
import re
FPS = 60
pygame.init()
icon = pygame.image.load("project_logo.png")  # Make sure the path is correct
pygame.display.set_icon(icon)


def pulse_image(surface, image, pos, original_size, time_start, speed=2.0, scale_range=0.2):
	"""
	Draws a pulsing image to the surface.
	
	:param surface: Pygame surface to draw on
	:param image: The original loaded image
	:param pos: Center position (x, y)
	:param original_size: (width, height) of original image
	:param time_start: reference start time for animation
	:param speed: pulses per second
	:param scale_range: percentage of scaling (+/-)
	"""
	elapsed = time.time() - time_start
	pulse = math.sin(elapsed * speed * 2 * math.pi)
	scale_factor = 1 + scale_range * pulse

	new_size = (
		int(original_size[0] * scale_factor),
		int(original_size[1] * scale_factor)
	)
	scaled_img = pygame.transform.smoothscale(image, new_size)
	draw_pos = (
		pos[0] - new_size[0] // 2,
		pos[1] - new_size[1] // 2
	)
	surface.blit(scaled_img, draw_pos)
def render_clipped_text_input(screen, input_data, clip_length=100):
	full_text = input_data['visualizer'].manager.value
	clipped_text = full_text[-clip_length:]  # Show only the last `clip_length` chars

	# Render the clipped text surface
	font = input_data['visualizer'].font_object
	font_color = input_data['visualizer'].font_color
	surface = font.render(clipped_text, True, font_color)

	# Blit it to the screen
	screen.blit(surface, input_data['pos'])
	
	# Optionally draw the rect if active
	pygame.draw.rect(screen, (150, 150, 150), input_data['rect'], 1)

# Function to set up the text input boxes
def setup_text_inputs():
	text_inputs = {}
	textbox_width = 250
	# States
	text_inputs['states'] = {
		'visualizer': TextInputVisualizer(
			manager=TextInputManager(initial="q0,q1,q2"),
			font_object=pygame.font.Font(font_path, font_size),
			font_color=(255, 0, 0)
			
		),
		'pos': (10, 80),
		'rect': pygame.Rect(8, 80, 250, 36),
		'label': 'States (e.g., 1,2,3)',
		'label_pos': (10, 52)
	}
	
	# Alphabet
	text_inputs['alphabet'] = {
		'visualizer': TextInputVisualizer(
			manager=TextInputManager(initial="a,b,c"),
			font_object=pygame.font.Font(font_path, font_size),
			font_color=(0, 255, 0)
		),
		'pos': (10, 170),
		'rect': pygame.Rect(8, 170, 250, 36),
		'label': 'Alphabet (e.g., 0,1)',
		'label_pos': (10, 142)
	}
	
	# Transitions
	text_inputs['transitions'] = {
		'visualizer': TextInputVisualizer(
			manager=TextInputManager(initial="(q0,q1,a),(q1,q2,b),(q2,q0,c)"),
			font_object=pygame.font.Font(font_path, font_size),
			font_color=(0, 0, 255)
		),
		'pos': (10, 260),
		'rect': pygame.Rect(8, 260, 250, 36),
		'label': 'Transitions (e.g., (s,n,a))',
		'label_pos': (10, 232)
	}
	
	# Start State
	text_inputs['start'] = {
		'visualizer': TextInputVisualizer(
			manager=TextInputManager(initial="q0"),
			font_object=pygame.font.Font(font_path, font_size),
			font_color=(255, 255, 0)
		),
		'pos': (10, 350),
		'rect': pygame.Rect(8, 350, 250, 36),
		'label': 'Start State (e.g., 1)',
		'label_pos': (10, 322)
	}
	
	# Final States
	text_inputs['final'] = {
		'visualizer': TextInputVisualizer(
			manager=TextInputManager(initial=r"q2"),
			font_object=pygame.font.Font(font_path, font_size),
			font_color=(255, 0, 255)
		),
		'pos': (10, 440),
		'rect': pygame.Rect(8, 438, 250, 36),
		'label': 'Final States (e.g.,q0,q1)',
		'label_pos': (10, 410)
	}
	
	return text_inputs

# Function to render the UI
def render_ui(text_inputs, active_textinput, pulse_time, NfaFlag):
	# Draw dividers and background elements
	draw_pulsating_divider(288, 0, 10, 750, pulse_time)
	draw_pulsating_divider(750, 0, 10, 750, pulse_time)
	pygame.draw.rect(screen, WHITE, (0, 0, 280, 1000), width=0)

	# Draw labels and text boxes
	for key, input_data in text_inputs.items(): 
		draw_text_with_stroke(input_data['label'], font, BLACK, input_data['label_pos'])
		#screen.blit(input_data['visualizer'].surface, input_data['pos'])
		render_clipped_text_input(screen, input_data, clip_length=26)

		if active_textinput == input_data['visualizer']:
			pygame.draw.rect(screen, input_data['visualizer'].font_color, input_data['rect'], 2)

	# Draw the submit button
	pygame.draw.rect(screen, (0, 255, 0), submit_button_rect)
	draw_text_with_stroke('Submit', font, BLACK, (110, 500))


# Function to handle text input focus
def handle_text_input_focus(events, text_inputs, active_textinput):
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = event.pos
			for key, input_data in text_inputs.items():
				if input_data['rect'].collidepoint(mouse_pos):
					active_textinput = input_data['visualizer']
					break
			else:
				active_textinput = None
	return active_textinput

def transition_adapter_to_machine(transitions):#expect argument->['input','next','alphabet']
	trans_output={}
	for transition in transitions:
		if transition[2] == 'e':
			
			trans_output.update({(transition[0],'ε'):{transition[1]}})
		else:
			trans_output.update({(transition[0],transition[2]):{transition[1]}})
	return trans_output

def states_adapter(states):#expect argument->{frozenset(), frozenset({'q0'}), frozenset({'q2'}), frozenset({'q1'})}
	states_output=set({})
	for s in states:
		
		states_output.update(s)
	
	return states_output

def start_state_adapter(state):#expected to be a frozenset
	return str(next(iter(set({}).union(state))))

def transition_adapter_from_machine(transitions):
	output=[]
	inp=''
	nex=''
	alpha=''
	for trkey,trValue in transitions.items():#tr : {(frozenset({'q0'}), 'b'): frozenset()}
		inp=str((trkey[0]))
		nex=trValue
		alpha=trkey[1]
		if nex == frozenset() or nex == 'frozenset()':
			nex='ϕ'
		else:
			nex= next(iter((nex)))
		if inp == 'frozenset()' or inp == frozenset() :
			inp='ϕ'
		else:
			inp= next(iter(eval(inp)))
		
	   
		output.append((inp,nex,alpha))
	   #print(output)
		
		  #output.append((list(tr.keys())[0][0],tr[tr.keys()],list(tr.keys())[0][1]))
	return output
   
   
def parse_tuple_set(input_str):
	# Remove outer parentheses if they exist
	input_str = input_str.strip()
	
	# Use regex to extract tuples
	import re
	matches = re.findall(r'\(([^)]+)\)', input_str)

	result = set()
	for match in matches:
		parts = tuple(part.strip() for part in match.split(','))
		result.add(parts)
	
	return result
def contains_phi(data):
	# Return True if 'ϕ' is found in any tuple, otherwise False
	return any('ϕ' in tup for tup in data)
# Function to draw the NFA (unchanged)
def generate_nfa_graph(states, transitions, alphabet,start_state, final_states, filename="nfa_graph"):
	dot = Digraph(format='png')
	for state in states:
		if state in final_states:
			dot.node(state, shape="doublecircle")
		else:
			dot.node(state, shape="circle")
	dot.node(start_state, color="red")
	for from_state, to_state, symbol in transitions:
		dot.edge(from_state, to_state, label=symbol)
	img_data = dot.pipe(format="png")
	
	
	#DFA equivalent
	dfa_output= NFA.NFA(states, alphabet, transition_adapter_to_machine(transitions), start_state, final_states).to_dfa()
	#states: states_adapter(dfa_output.states)
	#dfa_output.alphabet
	#start_state_adapter(dfa_output.start_state)
	#states_adapter(dfa_output.final_states)
	#transition_adapter_from_machine(dfa_output.transitions)
	
	#let's get the output image:
	
	dot1 = Digraph(format='png')
	if contains_phi(transition_adapter_from_machine(dfa_output.transitions)):
		states = dfa_output.states.union({'ϕ'})
		
	else:
		states = dfa_output.states
   
	for state in states_adapter(states):
		
		if state in states_adapter(dfa_output.final_states):
			dot1.node(state, shape="doublecircle")
		else:
			dot1.node(state, shape="circle")
			
	dot1.node(start_state_adapter(dfa_output.start_state), color="red")
	for from_state, to_state, symbol in transition_adapter_from_machine(dfa_output.transitions):
		dot1.edge(from_state, to_state, label=symbol)
	img_output_data = dot1.pipe(format="png")
	#print(transition_adapter_from_machine(dfa_output.transitions))
	#----------------------------------
	return pygame.image.load(io.BytesIO(img_data)),pygame.image.load(io.BytesIO(img_output_data))

# Test states (unchanged)
states = {"q0", "q1", "q2"}
transitions = [("q0", "q1", "a"), ("q1", "q2", "b"), ("q2", "q0", "c")]
start_state = "q0"
final_states = {"q2"}
alphabet={'a','b','c'}
nfa_image,dfa_image = generate_nfa_graph(states,transitions, alphabet, start_state, final_states)
nfa_image=pygame.transform.scale(nfa_image, (370, 400))
dfa_image=pygame.transform.scale(dfa_image, (600, 400))
current_frame = 0
animation_speed = 100  # Time in milliseconds between frames

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1500, 550))

CYAN = (0, 255, 255)
LIGHT_CYAN = (173, 216, 230)
BLACK = (0, 0, 0)
BLUE = (0, 255, 255)
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)

font_path = "AvenirLTProBook.otf"
font_size = 14
font = pygame.font.Font(font_path, font_size)
strock_font = pygame.font.Font(font_path, 19)

def draw_pulsating_divider(x, y, width, height, pulse_time):
	glow_intensity = int(5 + 5 * math.sin(pulse_time))
	pygame.draw.rect(screen, LIGHT_CYAN, (x - glow_intensity, y - glow_intensity, width + 2 * glow_intensity, height + 2 * glow_intensity))
	pygame.draw.rect(screen, CYAN, (x, y, width, height))

stroke_ctr = 0

	
def draw_text_with_stroke(text, font, text_color, position):
	text_surface = font.render(text, True, text_color)
	screen.blit(text_surface, position)

# Initial setup
pygame.display.set_caption("NFA to DFA simulator")
bg = pygame.image.load('bg.jpg')
bg = pygame.transform.smoothscale(bg, (1500, 550))

nfa_screen = pygame.image.load('NFA.png')
nfa_screen = pygame.transform.scale(nfa_screen, (120, 110))

dfa_screen = pygame.image.load('DFA.png')
dfa_screen = pygame.transform.scale(dfa_screen, (120, 110))

text_inputs = setup_text_inputs()
submit_button_rect = pygame.Rect(100, 490, 100, 40)

nfa_x = 500
nfa_y = 0
nfa_speed = 1
pulse_time = 0
exit = True
NfaFlag = True
DfaFlag = True
active_textinput = None
start_time = time.time()
# Main game loop

while exit:
	events = pygame.event.get()
	
	for event in events:
		if event.type == pygame.QUIT:
			exit = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if submit_button_rect.collidepoint(event.pos):
				#print('Im steve !!!!!!!!!!!!!!!!!')
				states = text_inputs['states']['visualizer'].manager.value
				alphabet = text_inputs['alphabet']['visualizer'].manager.value
				transitions = text_inputs['transitions']['visualizer'].manager.value
				start = text_inputs['start']['visualizer'].manager.value
				final = text_inputs['final']['visualizer'].manager.value
				#states: set(states.split(",")) 
				# print(set(states.split(",")))
				# print("-------------------------")
				# print(set(alphabet.split(",")))
				# print("-------------------------")
				print(parse_tuple_set(transitions))
				# print("-------------------------")
				# print(start)
				# print("-------------------------")
				# print(set(final.split(",")))
				# print("-------------------------")
				nfa_image,dfa_image = generate_nfa_graph(set(states.split(",")),parse_tuple_set(transitions), set(alphabet.split(",")), start, set(final.split(",")))
				nfa_image=pygame.transform.scale(nfa_image, (370, 400))
				dfa_image=pygame.transform.scale(dfa_image, (600, 400))
	# Handle text input focus
	active_textinput = handle_text_input_focus(events, text_inputs, active_textinput)

	# Update the active text box
	if active_textinput:
		active_textinput.update(events)

	current_time = pygame.time.get_ticks()
	pulse_time = (current_time * 4 / 1000)
	screen.blit(bg, (0, 0))
	
	#Dfa logo blitting
	#screen.blit(dfa_screen,(1100,0))
	pulse_image(screen, dfa_screen, (1100,60), (120, 110), start_time,1,0.1)
	#Nfa logo blitting
	screen.blit(nfa_screen, (nfa_x, nfa_y))
	if NfaFlag:
		nfa_x += 1
		if nfa_x > 640:
			NfaFlag = False
	elif not NfaFlag:
		nfa_x -= 1
		if nfa_x < 290:
			NfaFlag = True

	# Render the UI (replaces the manual drawing of dividers, rectangle, and text)
	render_ui(text_inputs, active_textinput, pulse_time, NfaFlag)

	# Draw the NFA graph (unchanged for now)
	screen.blit(nfa_image, (350, 130))
	screen.blit(dfa_image, (810, 120))
	clock.tick(FPS)
	pygame.display.update()


pygame.quit()


# import pygame
# import math
# import time
# import re
# from NFA import NFA

# # Constants
# FPS = 60
# WINDOW_SIZE = (800, 600)
# FONT_PATH = "pixel.TTF"
# FONT_SIZE = 14

# # Colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# CYAN = (0, 255, 255)
# LIGHT_CYAN = (173, 216, 230)


# class InputBox:
#     """
#     A simple text input box for pygame.
#     """
#     def __init__(self, rect, font, initial_text=""):
#         self.rect = pygame.Rect(rect)
#         self.font = font
#         self.text = initial_text
#         self.is_active = False
#         self.color_inactive = (150, 150, 150)
#         self.color_active = (0, 255, 0)

#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             self.is_active = self.rect.collidepoint(event.pos)
#         if event.type == pygame.KEYDOWN and self.is_active:
#             if event.key == pygame.K_BACKSPACE:
#                 self.text = self.text[:-1]
#             else:
#                 self.text += event.unicode

#     def draw(self, surface):
#         color = self.color_active if self.is_active else self.color_inactive
#         pygame.draw.rect(surface, color, self.rect, 2)
#         txt_surf = self.font.render(self.text, True, WHITE)
#         surface.blit(txt_surf, (self.rect.x + 5, self.rect.y + 5))


# class AutomataApp:
#     def __init__(self):
#         pygame.init()
#         self.clock = pygame.time.Clock()
#         self.screen = pygame.display.set_mode(WINDOW_SIZE)
#         pygame.display.set_caption("NFA to DFA Simulator")
#         self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

#         # Input fields
#         self.input_states = InputBox((20, 20, 200, 30), self.font, "q0,q1,q2")
#         self.input_alphabet = InputBox((20, 70, 200, 30), self.font, "a,b,c")
#         self.input_transitions = InputBox((20, 120, 200, 30), self.font, "(q0,q1,a),(q1,q2,b)")
#         self.input_start = InputBox((20, 170, 200, 30), self.font, "q0")
#         self.input_final = InputBox((20, 220, 200, 30), self.font, "q2")

#         self.inputs = [
#             self.input_states,
#             self.input_alphabet,
#             self.input_transitions,
#             self.input_start,
#             self.input_final,
#         ]

#     def parse_transitions(self, text: str):
#         # Simplified tuple parsing
#         matches = re.findall(r"\(([^)]+)\)", text)
#         transitions = []
#         for match in matches:
#             parts = [p.strip() for p in match.split(',')]
#             if len(parts) == 3:
#                 transitions.append(tuple(parts))
#         return transitions

#     def run(self):
#         running = True
#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 for input_box in self.inputs:
#                     input_box.handle_event(event)

#             self.screen.fill(BLACK)
#             # Draw input boxes
#             for box in self.inputs:
#                 box.draw(self.screen)

#             # TODO: draw NFA and DFA visualizations

#             pygame.display.flip()
#             self.clock.tick(FPS)

#         pygame.quit()


# if __name__ == "__main__":
#     AutomataApp().run()
