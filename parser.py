from textx import metamodel_from_file
import webcolors
from pprint import pprint

try:
    map_grammar = metamodel_from_file('./map_grammar.tx')
    map_model = map_grammar.model_from_file('./test.txt');
    pprint(map_model.hubs[1].__dict__)
    pprint(map_model.hubs[1].meta[0].__dict__)
except Exception as e:
    print(e)
