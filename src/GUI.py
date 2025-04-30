import pygame
import pygame_textinput
from graphviz import Digraph
import pyperclip
import unicodedata
import io
from NFA import NFA
from DFA import DFA
FPS = 60
WINDOW_SIZE = (854, 480)
FONT_PATH = "arial unicode ms.otf"
FONT_SIZE = 14
BG_IMAGE = 'bg.jpg'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 234, 255)


class AutomatonVisualizer:
	def __init__(self, machine: NFA, screen, pos, size):
		self.machine = machine
		self.screen = screen
		self.pos = pos
		self.size = size
		self.image = None
		self.create_graphs()
		
		# Load overlay images
		self.nfa_overlay = pygame.image.load('NFA.png').convert_alpha()
		self.dfa_overlay = pygame.image.load('DFA.png').convert_alpha()
		overlay_size = (80, 30)  # Adjust as needed
		self.nfa_overlay = pygame.transform.smoothscale(self.nfa_overlay, overlay_size)
		self.dfa_overlay = pygame.transform.smoothscale(self.dfa_overlay, overlay_size)

	def create_graphs(self):
		dot_nfa = Digraph(format='png', engine='dot')
		dot_nfa.attr(dpi='300')

		for state in self.machine.states:
			shape = 'doublecircle' if state in self.machine.final_states else 'circle'
			dot_nfa.node(state, shape=shape)
		dot_nfa.node(self.machine.start_state, color='red')
		for (src, sym), dests in self.machine.transitions.items():
			for dst in dests:
				dot_nfa.edge(src, dst, label=sym)
		nfa_img = dot_nfa.pipe(format='png')

		dfa: DFA = self.machine.to_dfa()
		dot_dfa = Digraph(format='png', engine='dot')
		dot_dfa.attr(dpi='300')
		for state in dfa.states:
			label = 'Δ' if not state else '{' + ','.join(sorted(state)) + '}'
			shape = 'doublecircle' if state in dfa.final_states else 'circle'
			dot_dfa.node(label, shape=shape)
		start_label = '{' + ','.join(sorted(dfa.start_state)) + '}'
		dot_dfa.node(start_label, color='red')
		for (src, sym), dst in dfa.transitions.items():
			src_label = 'Δ' if not src else '{' + ','.join(sorted(src)) + '}'
			dst_label = 'Δ' if not dst else '{' + ','.join(sorted(dst)) + '}'
			dot_dfa.edge(src_label, dst_label, label=sym)
		dfa_img = dot_dfa.pipe(format='png')

		raw_nfa = pygame.image.load(io.BytesIO(nfa_img))
		raw_dfa = pygame.image.load(io.BytesIO(dfa_img))
		self.nfa_image = pygame.transform.scale(raw_nfa, self.size)
		self.dfa_image = pygame.transform.scale(raw_dfa, self.size)
		self.nfa_image = pygame.transform.smoothscale(raw_nfa, self.size)
		self.dfa_image = pygame.transform.smoothscale(raw_dfa, self.size)

	def draw(self):
		# Draw the NFA image and overlay
		self.screen.blit(self.nfa_image, self.pos)
		self.screen.blit(self.nfa_overlay, (self.pos[0] + 10, self.pos[1] + 10))  # top-left of NFA

		# Draw the DFA image and overlay
		dfa_pos = (self.pos[0] + self.size[0] + 20, self.pos[1])
		self.screen.blit(self.dfa_image, dfa_pos)
		self.screen.blit(self.dfa_overlay, (dfa_pos[0] + 210, dfa_pos[1] + 10))  # top-left of DFA


class TextBox:
	def __init__(self, label, initial, pos, font):
		self.manager = pygame_textinput.TextInputManager(
			initial=initial, validator=lambda x: True
		)
		self.visualizer = pygame_textinput.TextInputVisualizer(
			manager=self.manager, font_object=font, font_color=BLACK
		)
		self.visualizer.cursor_color = BLACK
		self.rect = pygame.Rect(pos[0] - 2, pos[1], 175, 36)
		self.label = label
		self.pos = pos
		self.active = False

	def handle_click(self, pos):
		"""Handle mouse click events"""
		self.active = self.rect.collidepoint(pos)

	def handle_events(self, events):
		"""Handle keyboard events"""

		def is_valid_char(c):
			return (
				c.isprintable() and
				not unicodedata.category(c).startswith('C') and  # Control
				not unicodedata.category(c).startswith('Z')      # Separator
			)

		filtered_events = []
		for event in events:
			if event.type == pygame.KEYDOWN and self.active:
				# Handle Ctrl+V paste
				if event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
					try:
						clipboard_content = pyperclip.paste()
						if clipboard_content:

							cleaned_content = ''.join(
								c for c in clipboard_content if is_valid_char(c))

							cursor_pos = self.manager.cursor_pos
							text = self.manager.value

							new_text = text[:cursor_pos] + \
								cleaned_content + text[cursor_pos:]
							self.manager.value = new_text
							self.manager.cursor_pos = cursor_pos + \
								len(cleaned_content)
					except Exception as e:
						print(f"Error pasting from clipboard: {e}")
					finally:
						continue

			filtered_events.append(event)
		
		self.visualizer.update(filtered_events) # type: ignore

	def draw(self, screen):
		"""Draw the textbox and its label"""
		pygame.draw.rect(screen, WHITE, self.rect)
		pygame.draw.rect(screen, BLACK, self.rect, 1)
		try:
			text_surface = self.visualizer.surface
			screen.blit(text_surface, self.pos)
		except ValueError as e:
			print(f"Error rendering text: {e}")
			placeholder = self.visualizer.font_object.render(
				"(Invalid text)", True, BLACK)
			screen.blit(placeholder, self.pos)

		label_surf = self.visualizer.font_object.render(
			self.label, True, WHITE)
		screen.blit(label_surf, (self.pos[0], self.pos[1] - 20))

	@property
	def value(self):
		return self.manager.value


class NFAApp:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode(WINDOW_SIZE)
		pygame.display.set_caption("NFA to DFA Simulator")

		# Initializing clipboard support
		pygame.scrap.init()
		pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

		self.clock = pygame.time.Clock()
		self.bg = pygame.transform.smoothscale(
			pygame.image.load(BG_IMAGE), WINDOW_SIZE)
		self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
		self.textboxes = [
			TextBox('States (e.g., q0,q1)', 'q0,q1,q2', (10, 40), self.font),
			TextBox('Alphabet (e.g., a,b)', 'a,b,c', (10, 120), self.font),
			TextBox(
				'Transitions (e.g., (q0,q1,a) (q1,q2,b))', '(q0,q1,a) (q1,q2,b) (q2,q0,c)', (10, 200), self.font
			),
			TextBox('Start State', 'q0', (10, 280), self.font),
			TextBox('Final States', 'q2', (10, 360), self.font)
		]
		self.submit_button = pygame.Rect(47, 420, 100, 40)
		self.visualizer = None

	def parse(self):
		states = set(self.textboxes[0].value.split(','))
		alphabet = set(self.textboxes[1].value.split(','))
		transitions = {}
		import re

		transition_pattern = r'\(\s*([^,\s]+)\s*,\s*([^,\s]+)\s*,\s*([^,\s]+)\s*\)'
		matches = re.findall(transition_pattern, self.textboxes[2].value)

		for src, dst, sym in matches:
			key = (src.strip(), sym.strip())
			transitions.setdefault(key, set()).add(dst.strip())
		start = self.textboxes[3].value.strip()
		finals = set(self.textboxes[4].value.split(','))
		return NFA(states, alphabet, transitions, start, finals)

	def run(self):
		running = True
		while running:
			events = pygame.event.get()

			# Handle quit event
			for event in events:
				if event.type == pygame.QUIT:
					running = False

			# Handle mouse clicks
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					clicked = False

					# Handle textbox clicks
					for tb in self.textboxes:
						tb.handle_click(event.pos)
						if tb.active:
							clicked = True

					# Handle submit button click
					if self.submit_button.collidepoint(event.pos):
						nfa = self.parse()
						self.visualizer = AutomatonVisualizer(
							nfa, self.screen, (200, 0), (300, 480)
						)

			# Handle keyboard events for active textboxes
			for tb in self.textboxes:
				if tb.active:
					tb.handle_events(events)

			# Draw everything
			self.screen.blit(self.bg, (0, 0))
			for tb in self.textboxes:
				tb.draw(self.screen)

			# Draw submit button
			pygame.draw.rect(self.screen, CYAN, self.submit_button)
			submit_surf = self.font.render('Submit', True, BLACK)
			self.screen.blit(
				submit_surf, (self.submit_button.x + 27,
							  self.submit_button.y + 10)
			)

			# Draw visualizer if exists
			if self.visualizer:
				self.visualizer.draw()

			pygame.display.update()
			self.clock.tick(FPS)

		pygame.quit()


if __name__ == '__main__':
	NFAApp().run()
