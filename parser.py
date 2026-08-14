from textx import metamodel_from_file

try:
    map_grammar = metamodel_from_file('./map_grammar.tx')
    map_model = map_grammar.model_from_file('./test.txt');
    print(map_model.nb_drones)
except Exception as e:
    print(e)
