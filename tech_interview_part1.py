from string import punctuation
import sys

class TextProcessor(object):
	def __init__(
		self,
		text
	):
		"""
		This object is used to process text as the specifications of the document
		"""
		self.text = text

	def filteredLinesStats(self, 
			keyWords={"/product/", "/produit/", "/catalog"},
			isStrict=True
		):
		"""
		Returns the number of lines containing the keywords in the given text
		Returns the total number of the numbers withing the filtered lines
		Returns the average number of the numbers within the filtered lines
		"""

		f_lines = self.filterLines()

		numbers = []
		for l in f_lines:
			numbers.extend(self.extractNumbers(l, isStrict))

		return len(f_lines), self.numberStats(numbers)

	def filterLines(self, keywords=["/product/", "/produit/", "/catalog"]):
		"""
		Returns only the lines containing the given keywords, and that don't
			start with '#' or ';'
		"""
		filtered_lines = []
		improperStarters = {"#", ";"}
		lines = self.text.split("\n")

		for l in lines:
			if len(l) > 0:
				if l[0] not in improperStarters:
					if any(w in l for w in keywords):
						filtered_lines.append(l)


		return filtered_lines

	def numberStats(self, numbers):
		"""
		Gives the total of a list of numbers and it's average
		"""
		total = 0
		average = 0
		for n in numbers:
			total += n

		if len(numbers) != 0:
			average = total / len(numbers)

		return average, total

	def extractNumbers(self, text, isStrict=True):
		"""
		Extract all numbers from text.
		Optional parameter isStrict. If set to True, will only extract numbers
			not surrounded by letters. If set to False, will extract all possible numbers
			Example: "My name is Michel3, I am ~19 years old". isStrict will extract [19]
				isStrict=False will extract [3, 19]
		"""
		numbers = []
		if isStrict:
			for w in text.split():
				try:
					w = w.strip(punctuation)
					number = float(w)
					numbers.append(number)
				except ValueError:
					pass
		else:
			number = ""
			wasDigit = False
			wasDecimal = False
			for c in text:
				try:
					digit = int(c)
					wasDigit = True
					number += c
				except ValueError:
					if c == '.':
						if wasDigit == True:
							if wasDecimal == False:
								number += c
								wasDecimal = True
							else:
								wasDecimal = False
								wasDigit = False
								try:
									numbers.append(float(number))
									number = ""
								except ValueError:
									pass
					else:

						wasDecimal = False
						wasDigit = False
						try:
							numbers.append(float(number))
							number = ""
						except ValueError:
							pass

		return numbers

	def countWords(self):
		"""
		Counts the number of words in a given text. Words are delimited by
			whitespace and new lines
		"""
		return len(self.tokenize())

	def tokenize(self):
		"""
		tokenizes the given text delimited by whitespaces and new lines
		"""
		return self.text.split()

if __name__ == "__main__":
	filename = sys.argv[1]

	with open(filename) as f:
		text = f.read()

	print(text)

	tp = TextProcessor(text)
	numWords = tp.countWords()
	all_average, all_sum = tp.numberStats(tp.extractNumbers(tp.text))
	num_filtered_lines, (filtered_lines_average, filtered_lines_total) = tp.filteredLinesStats()

	print("Number of words: {0}\nTotal average of numbers: {1}\nTotal sum of numbers: {2}\nNumber of lines containing '/product/', '/produit/', '/catalog': {3}\n"
		.format(numWords, all_average, all_sum, num_filtered_lines))
	print("Average of numbers in previous lines: {0}\nTotal of numbers in previous lines {1}\n".format(filtered_lines_average, filtered_lines_total))


