class Procedure_depr:
	def __init__(self, first):
		self.base_sequence = ['B', 'B', 'P', 'P', 'B', 'B', 'P', 'P', 'B', 'P']
		self.first = first
		self.second = 'D' if first == 'R' else 'R'

	def start(self):
		for step in self.base_sequence:
			yield self.first+step, self.__create_message__(self.first+step)
			yield self.second+step, self.__create_message__(self.second+step)

		raise StopIteration

	def __create_message__(self, action):
		message = 'Radiants' if action[0] == 'R' else 'Dires'
		message += ' turn to '
		message += 'pick' if action[1] == 'P' else 'ban'
		message += '!'
		return message

	def __iter__(self):
		return self.start()


class AllPickProcedure:
	def __init__(self, first):
		self.base_sequence = ['P', 'P', 'P', 'P', 'P', 'B']
		self.order = [{'R': 'D', 'D': 'R'}[first]]
		self.step = -1

	def __step__(self):
		if self.step >= 6 or self.step < 0:
			raise StopIteration
		action = self.order[0] + self.base_sequence[self.step]
		return action, self.__create_message__(action)

	def next(self):
		self.step += 1
		return self.__step__()

	def previous(self):
		self.step -= 1
		return self.__step__()

	def current_step(self):
		return self.__step__()

	def expose_step(self):
		return {'R': 'D', 'D': 'R'}[self.order[0]] + self.base_sequence[0]

	def switch_order(self):
		return AllPickProcedure(self.order[0])

	def __create_message__(self, action):
		message = 'Radiants' if action[0] == 'R' else 'Dires'
		message += ' turn to '
		message += 'pick'
		message += '!'
		return message

	def __iter__(self):
		return self


class CaptainsModeProcedure:
	def __init__(self, first):
		self.base_sequence = ['B', 'B', 'P', 'P', 'B', 'B', 'P', 'P', 'B', 'P']
		self.order = [first]
		self.order += ['D'] if first == 'R' else ['R']
		self.step = -1

	def __step__(self):
		if self.step >= 20 or self.step < 0:
			raise StopIteration
		action = self.order[self.step%2] + self.base_sequence[self.step/2]
		return action, self.__create_message__(action)

	def next(self):
		self.step += 1
		return self.__step__()

	def previous(self):
		self.step -= 1
		return self.__step__()

	def current_step(self):
		return self.__step__()

	def expose_step(self):
		return self.order[self.step%2] + self.base_sequence[self.step/2]

	def switch_order(self):
		mapping = {'R': 'D', 'D': 'R'}
		return CaptainsModeProcedure(mapping[self.order[0]])

	def __create_message__(self, action):
		message = 'Radiants' if action[0] == 'R' else 'Dires'
		message += ' turn to '
		message += 'pick' if action[1] == 'P' else 'ban'
		message += '!'
		return message

	def __iter__(self):
		return self