
from owlready2 import *
import argparse
from IPython.display import display, Markdown, Latex
import editdistance

# CLI Arguments for specifying a Kilnform
parser = argparse.ArgumentParser(description='Process benchmarks.')
parser.add_argument("-m", "--materials", default=[], type=str, nargs='+',
                    help="The materials to be fired.")
parser.add_argument("-f", "--firing", default=210, type=int, 
                    help="The firing temperature of the kiln (default: Celsius).")
parser.add_argument("-T", "--temperature_unit", default='C', type=str,
                    help="C = Celsius, F= Fahrenheit, K=Kelvin")

parser.add_argument("-q", "--query", default="", type=str,
                    help="Query the Kilnforms Ontology")



def first_element(arr, default_value = None):
	if len(arr) > 0:
		return arr[0]
	else:
		default_value or "-"

def comma_list(arr):
	arr = map(lambda x: str(x), arr)
	return "\n* "+("\n* ".join(arr))
	
# Render Stretgy
def render_using_label(entity):
	return bold(f"{entity.name} ({entity.label.first()})") or entity.name

def render_query(entity):
	if entity.label.first():
		return bold(f"{entity.name} ({entity.label.first()})")
	else: 
		title = entity.name
		return title

# Search Ontology by Label
def queryPlasticByLabel(label):
	results = default_world.sparql(f"SELECT ?x {{ ?x rdfs:label '{label}' .}}")
	return list(results)[0][0]

# Equation 1
def computeMalleableForm(plastic, firingTemperature):
	Tg = onto.glassTransitionTemperature[plastic][0]
	Tm = onto.fusionTemperature[plastic][0]
	alpha = (firingTemperature - Tg) / (Tm - Tg)
	if firingTemperature/Tm > 2:
		return "DANGER", alpha, Tm, Tg

	if alpha <= 0: 
		return "Rigid", alpha, Tm, Tg
	elif alpha > 0 and alpha <= 0.8:
		return "Leather", alpha, Tm, Tg
	elif alpha > 0.8 and alpha <= 1.1:
		return "Honey", alpha, Tm, Tg
	elif alpha > 1.1:
		return "Liquid", alpha, Tm, Tg
	
def convertTemp(input_unit, output_unit, value, stringify=False):
	if input_unit == "F" and output_unit == "C":
		value = (value - 32) * 5.0/9.0 # Convert to Celsius
	elif input_unit == "K" and output_unit == "C":
		value = (value - 273.15) # Convert to Celsius
	elif input_unit == "C" and output_unit == "F":
		value = value * (9.0/5.0) + 32
	elif input_unit == "C" and output_unit == "F":
		value = (value + 273.15)
	elif input_unit == output_unit:
		value =  value

	if stringify:
		return "%2.2fº%s"%(value, output_unit)
	else:
		return value 

def bold(t):
	return f"\033[1m{t}\033[0m"
def blue(t):
	return f"\033[;34m{t}\033[0m"

def entity(query):
	return getattr(onto, query)

def json(query):
	entity = getattr(onto, query)
	header = entity.name
	if entity:
		if entity.shortForm:
			header = header + " ("+ ", ".join(entity.shortForm) + ")"
		comment = entity.comment.first()

		subclasses = getattr(entity, "subclasses", None)
		if subclasses:
			subclasses = list(entity.subclasses())


		instances = getattr(entity, "instances", None)
		if instances:
			instances = list(entity.instances())

		ancestors = getattr(entity, "ancestors", None)
		if ancestors:
			ancestors = list(entity.ancestors())
		return {"entity": header, 
			"comment": comment, 
			"subclasses": subclasses, 
			"instances": instances,
			"ancestors": ancestors,
		    "obj": entity
		}
	else:
		return query


def similar_search(query):
	query = "kilnforms"+query
	dictionary = map(lambda x: (editdistance.eval(str(x), query), x), master_dictionary)
	dictionary = list(dictionary)
	search_results = list(sorted(dictionary, key=lambda x: x[0]))[0:3]
	return list(map(lambda x: x[1], search_results))

def markdown_header(text, level):
	prefix = "#"*level
	md_header = prefix +" "+ str(text)
	display(Markdown(md_header))

def markdown_list(arr):
	if len(arr) == 0:
		display(Markdown("None found."))
	else:
		arr = map(lambda x: x.name, arr)
		md_list = "\n* "+("\n* ".join(arr))
		display(Markdown(md_list))

def markdown_paragraph(p):
	display(Markdown(str(p)))

def markdown_concept(concept):
	if type(concept) == str:
		markdown_paragraph("No concept matches found. Did you mean...")
		markdown_list(similar_search(concept))
	else:
		markdown_header(concept["entity"], 1)
		
		if concept["comment"]:
			markdown_header("Comments", 2)
			markdown_paragraph(concept["comment"])
		if concept["subclasses"]:
			markdown_header("Subclasses", 2)
			markdown_list(concept["subclasses"])
		if concept["ancestors"]:
			markdown_header("Parents", 2)
			markdown_list(concept["ancestors"])
		if concept["instances"]:
			markdown_header("Instances", 2)
			markdown_list(concept["instances"])

onto = get_ontology("kilnforms.owl").load()
master_dictionary = list(onto.classes()) + list(onto.individuals()) + list(onto.data_properties()) + list(onto.object_properties())

# args = parser.parse_args()

# if args.query != '':
# 	# KILNFORM QUERY
# 	print("QUERY", args.query)
# 	set_render_func(render_query)
# 	entity = getattr(onto, args.query)
# 	comment = entity.comment.first()
# 	subclasses = comma_list(entity.subclasses())
# 	instances = comma_list(entity.instances())


# 	print(bold(entity))
# 	print(f'''---------
# Comment: {comment}

# Subclasses: {subclasses}

# Instances: {instances}
# ''')


# else:
# 	# KILNFORM CALCULATOR
# 	set_render_func(render_query)
# 	alt = "F" if args.temperature_unit == "C" else "C"
# 	firing = convertTemp(args.temperature_unit, "C", args.firing)
# 	firingStrInternal = convertTemp(args.temperature_unit, "C", args.firing, True)
# 	firingStr = convertTemp(args.temperature_unit, args.temperature_unit, args.firing, True)
# 	firingStrAlt = convertTemp(args.temperature_unit, alt, args.firing, True)


# 	print("--------------------------\n")
# 	title = bold("Kilnform MalleableForm Calculator")
# 	print(title, "\n  Materials:", args.materials, "\n ", f"Firing at {firingStr} ({firingStrAlt})")
# 	print("\n-------------RESULTS--------------")

# 	for label in args.materials:
# 		plastic = queryPlasticByLabel(label)
# 		form, alpha, Tm, Tg = computeMalleableForm(plastic, args.firing)
# 		Tm = convertTemp("C", args.temperature_unit, Tm, True)
# 		Tg = convertTemp("C", args.temperature_unit, Tg, True)
# 		alpha = '%2.2f'%(alpha)
# 		form = blue(form)
# 		print(plastic,"\n  ", f"alpha: {alpha}", "\n  ", f"Tg: {Tg}", "\n  ", f"Tm: {Tm}", "\n  ", f"malleable_form: {form}",)

# 	print("---------------------------\n")

