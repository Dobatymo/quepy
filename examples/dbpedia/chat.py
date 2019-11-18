from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime, date, timedelta

import quepy
from SPARQLWrapper import SPARQLWrapper, JSON

class ParseError(Exception):
	pass

class NoAnswer(Exception):
	pass

def extract_define(results, target, metadata=None, lang="en"):
	defines = []

	for result in results["results"]["bindings"]:
		if result[target]["xml:lang"] == lang:
			defines.append(result[target]["value"])

	return defines

def extract_enum(results, target, metadata=None, lang="en"):
	labels = []

	for result in results["results"]["bindings"]:
		if result[target]["type"] == "literal":
			if result[target]["xml:lang"] == lang:
				labels.append(result[target]["value"])

	return labels

def extract_literal(results, target, metadata=None):
	literals = []

	for result in results["results"]["bindings"]:
		literal = result[target]["value"]
		if metadata:
			literals.append(metadata.format(literal))
		else:
			literals.append(literal)

	return literals

def extract_area(results, target, metadata=None):
	literals = []

	for result in results["results"]["bindings"]:
		literal = result[target]["value"]
		literals.append(literal + " square meter")

	return literals

def extract_time(results, target, metadata=None):
	times = []

	now = datetime.utcnow()
	for result in results["results"]["bindings"]:
		offset = result[target]["value"].replace("−", "-")

		if ("to" in offset) or ("and" in offset):
			if "to" in offset:
				connector = "and"
				from_offset, to_offset = offset.split("to")
			else:
				connector = "or"
				from_offset, to_offset = offset.split("and")

			from_offset, to_offset = int(from_offset), int(to_offset)

			if from_offset > to_offset:
				from_offset, to_offset = to_offset, from_offset

			from_delta = timedelta(hours=from_offset)
			to_delta = timedelta(hours=to_offset)

			from_time = now + from_delta
			to_time = now + to_delta

			retstr = "Between {} {} {}, depending on {}.".format(
				from_time.strftime("%H:%M"),
				connector,
				to_time.strftime("%H:%M on %A"),
				"your location"
			)
			times.append(retstr)

		else:
			offset = int(offset)
			the_time = now + timedelta(hours=offset)
			times.append(the_time.strftime("%H:%M on %A"))

	return times

def extract_age(results, target, metadata=None):
	ages = []

	now = datetime.utcnow()
	for result in results["results"]["bindings"]:

		birth_date = result[target]["value"]
		birth_date = datetime.strptime(birth_date, "%Y-%m-%d")

		age = now - birth_date
		ages.append("{} years old".format(age.days // 365))

	return ages

class DBPediaQuepy(object):

	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	dbpedia = quepy.install("dbpedia")

	def __init__(self, debug=False):

		if debug:
			quepy.set_loglevel("DEBUG")

		self.query_type_handlers = {
			"define": extract_define,
			"enum": extract_enum,
			"time": extract_time,
			"literal": extract_literal,
			"age": extract_age,
			"area": extract_area,
		}

	def get_query(self, question):
		# type: (str, ) -> Tuple[Any, Any, Any, Any]

		target, query, metadata = self.dbpedia.get_query(question)

		if query is None:
			raise ParseError(question)

		if isinstance(metadata, tuple):
			query_type = metadata[0]
			metadata = metadata[1]
		else:
			query_type = metadata
			metadata = None

		if target.startswith("?"):
			target = target[1:]

		return query, query_type, target, metadata

	def handle_query(self, query):
		# type: (str, ) -> Any

		self.sparql.setQuery(query)
		self.sparql.setReturnFormat(JSON)
		results = self.sparql.query().convert()

		if not results["results"]["bindings"]:
			raise NoAnswer(query, results)

		return results

	def respond(self, question):
		query, query_type, target, metadata = self.get_query(question)
		print(query)
		#print(query_type, target, metadata)
		results = self.handle_query(query)
		return self.query_type_handlers[query_type](results, target, metadata)

"""
working:
time in <country>?
what is the time in <country>?
what time is it in <country>?
How old is <person>?
Who is <person>?
Where is the <thing>?
What is the capital of <populated place>?
What is the population of <populated place>?
What is the area of <populated place>?
Where is <person> from?
What are the members of <band>?
List albums of <artist>.
list movies by <director>
How long is <movie>
Who is the director of <movie>

not working:
time in <city>
what is the age of <person>
when was <person> born

buggy:
how old is <dead person>

"""

if __name__ == "__main__":
	default_questions = [
		"What is a car?",
		"Who is Tom Cruise?",
		"Who is George Lucas?",
		"Who is Mirtha Legrand?",
		# "List Microsoft software",
		"Name Fiat cars",
		"time in Argentina",
		"what time is it in Chile?",
		"List movies directed by Martin Scorsese",
		"How long is Pulp Fiction",
		"which movies did Mel Gibson starred?",
		"When was Gladiator released?",
		"who directed Pocahontas?",
		"actors of Fight Club",
	]

	bot = DBPediaQuepy()
	while True:
		try:
			q = input(">")
			answer = bot.respond(q)
			if len(answer) == 1:
				print(answer[0])
			else:
				print(answer)

		except ParseError as e:
			print("ParseError", e)
		except NoAnswer as e:
			print("Sorry, I cannot find an answer for this question.")

	for q in default_questions:
		print(bot.respond(q))
