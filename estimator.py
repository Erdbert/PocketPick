class Estimator:
	def __init__(self, pool):
		self.pool = pool

	def estimate(self, opp):
		estimation = []
		for hero in [h for h in self.pool if h.isEnabled()]:
			adv = 0
			for opphero in opp:
				count = 0
				adv2 = 0
				try:
					adv2 += hero.related_to[opphero.name]
				except KeyError:
					pass
				else:
					count += 1.0

				try:
					adv2 -= opphero.related_to[hero.name]
				except KeyError:
					pass
				else:
					count += 1.0

				try:
					adv += adv2/count
				except ZeroDivisionError:
					pass

			estimation.append((hero, adv))

		return sorted(estimation, key=lambda x: (x[1], x[0]), reverse=True)