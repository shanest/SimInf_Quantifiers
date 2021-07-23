import json
from os import path
from pydoc import locate
import siminf.operator as op
from siminf import fileutil
from siminf.fileutil import FileUtil 


class ExperimentSetup:
    def __init__(self, props):
        self._props = props       # private
        # common setups 
        self.name = props['name']
        self.pareto_name = props['pareto_name']
        self.natural_name = props['natural_name']
        self.random_name = props['random_name']
        
        self.lexical_quantifiers_filename = \
            path.join(path.dirname(props['setup_filename']), props['lexical_quantifiers_filename'])
        self.generate_models = locate(props['model_generator'])
        self.generate_primitives = locate(props['primitive_generator'])
        self.parse_primitive = locate(props['primitive_parser'])
        self.measure_expression_complexity = locate(props['expression_complexity_measurer'])
        self.measure_quantifier_complexity = locate(props['quantifier_complexity_measurer'])
        self.operators = {name: op.operators[name] for name in props['operators']}
            
        self.natural_languages_dirname = \
            path.join(path.dirname(props['setup_filename']), 'Languages/{0}'.format(props['name']))
            
        self.possible_input_types = []
        for (name, operator) in self.operators.items():
            self.possible_input_types.append(operator.inputTypes)
            
        #set up of quantifiers, sizes, etc
        self.max_quantifier_length = int(props['max_quantifier_length'])
        self.model_size = int(props['model_size'])
        self.processes = int(props['processes'])
        # self.run_name = props['run_name']
        self.comp_strat = props['comp_strat']
        self.inf_strat = props['inf_strat']
        self.max_words = props['max_words']
            
        #set up of files
        self.dest_dir = props['dest_dir']
        self.use_base_dir = True if props['use_base_dir'].lower() == "true" else False
        
        self.dirname = fileutil.base_dir(self.dest_dir, self.name, self.max_quantifier_length, self.model_size) \
                if self.use_base_dir else \
            fileutil.run_dir(self.dest_dir, self.name, self.max_quantifier_length, self.model_size, self.run_name)
            
        self.file_util = FileUtil(self.dirname)
        
    def __len__(self):
        return len(self._props)
    
    def __getitem__(self, key):
        if key in self._props:
            return self._props[key]
        else: 
            return None
    
    def __iter__(self):
        for key in self._props.keys():
            yield key
        
            
    def __str__(self):
        repr =   '  ' + '======= common setups =======' \
             + '\n  ' + 'name: {0.name}'.format(self) \
             + '\n  ' + 'lexical_quantifiers_filename: {0.lexical_quantifiers_filename}'.format(self) \
             + '\n  ' + 'natural_languages_dirname: {0.natural_languages_dirname}'.format(self) \
             + '\n  ' + 'generate_models: {0.generate_models}'.format(self) \
             + '\n  ' + 'generate_primitives: {0.generate_primitives}'.format(self)  \
             + '\n  ' + 'operators: {0}'.format(self._props['operators']) \
             + '\n  ' + 'parse_primitive: {0}'.format(self.parse_primitive) \
             + '\n  ' + 'measure_expression_complexity: {0}'.format(self.measure_expression_complexity) \
             + '\n  ' + 'measure_quantifier_complexity: {0}'.format(self.measure_quantifier_complexity) \
                                                                                                         \
             + '\n  ' + '======= quantifiers, sizes, etc =======' \
             + '\n  ' + 'max_quantifier_length: {0}'.format(self.max_quantifier_length)  \
             + '\n  ' + 'model_size: {0}'.format(self.model_size)  \
             + '\n  ' + 'dest_dir: {0}'.format(self.dest_dir)  \
             + '\n  ' + 'processes: {0}'.format(self.processes)  \
             + '\n  ' + 'run_name: {0}'.format(self.run_name)  \
                                                               \
             + '\n  ' + '======= results =======' \
             + '\n  ' + 'use_base_dir: {0}'.format(self.use_base_dir) \
             + '\n  ' + 'dirname: {0}'.format(self.dirname) \
             + '\n  ' + 'file_util: {0}'.format(self.file_util)
                 
          
        return repr
    
    def show_loaded_setups(self):
        print("loaded setups")
        for (k, v) in self._props.items():
            print ("  {0} = {1}".format(k, v))
    
    def show_parsed_setups(self):
        print("parsed setups")
        print(self)
        

    def loaded_setups(self):
        return self._props
    
        
def parse(filename):
    props = {}
    with open(filename) as file:
        props = json.load(file)
    props['setup_filename'] = filename
    setup = ExperimentSetup(props)
    return setup
