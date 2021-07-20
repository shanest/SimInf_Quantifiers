
# Simplicity vs. Informativeness trade-off for quantifiers

This code accompanies XXX.  

**Acknowledgments:** The code was initially developed by Wouter Posdijk for his MSc Logic thesis in Amsterdam (see the repo this is forked from).  Qi C Guo also provided significant development time.

The code consists of the following parts:

Generation:

- Expression generation from a grammar
- Generating quantifiers with presupposition by combining expressions
- Sampling expressions into languages
- Generating optimal languages using an evolutionary algorithm

Measuring of expressions:

- Simplicity
- Informativeness
- Monotonicity
- Conservativity

Measuring of quantifiers with presupposition:

- Simplicity
- Informativeness

Measuring of languages:

- Simplicity
- Informativeness
- Monotonicity
- Conservativity
- Naturalness
- Optimality wrt a Pareto front


## Requirements

Python >=3.5. Get the required packages by running `pip install`.

Or: 
```
conda create --name siminf python=3.7
conda activate siminf
conda install --file requirements.txt -c conda-forge
```


## Running the code

Almost all code requires three main parameters:

- A path to the _Experiment Setup_ (see the folder ExperimentSetups). This specifies the grammar, using operators from [`Operator.py`](Code/Operator.py)
- The model size
- The maximum quantifier length

This will put the results of said code in results/[ExperimentSetupName]\_length=[length]\_size=[size]

### Replicating the experimental results

`export PYTHONPATH=$PYTHONPATH:./`

`python bin/individual_quantifiers/generate.py --setup experiment_setups/final.json --max_quantifier_length 4 --model_size 4`

`python bin/individual_quantifiers/measure_expression_complexity.py --setup experiment_setups/final.json --max_quantifier_length 4 --model_size 4`

`python bin/individual_quantifiers/measure_expression_monotonicity.py --setup experiment_setups/final.json --max_quantifier_length 4 --model_size 4`

`python bin/individual_quantifiers/measure_expression_conservativity.py --setup experiment_setups/final.json --max_quantifier_length 4 --model_size 4`


`python bin/individual_quantifiers/generate_natural_expressions.py --setup experiment_setups/final.json --max_quantifier_length 4 --model_size 4  `


`python bin/languages/generate_evolutionary.py --setup=experiment_setups/final.json --max_quantifier_length=4 --model_size=4 --lang_size=8 --sample_size=16 --generations=2 --max_mutations=2 --name=evolutionary`


#### generate languages with varying degrees of naturalness

`python bin/languages/sample_indexset_degrees.py --setup experiment_setups/final.json --max_quantifier_length 4 --model_size 4 --indices natural --name natural_gradual --max_words 5 --sample 100`

#### measure complexity and informativeness

`python bin/languages/measure.py --setup experiment_setups/final.json --max_quantifier_length 4 --model_size 4 --max_words=5 --name natural_gradual --comp_strat wordcomplexity --inf_strat simmax`

#### measure monotonicity and conservativity

`python bin/languages/measure_monotonicity.py --setup experiment_setups/final.json --max_quantifier_length 4 --model_size 4 --name natural_gradual`

`python bin/languages/measure_conservativity.py --setup experiment_setups/final.json --max_quantifier_length 4 --model_size 4 --name natural_gradual`


#### analysis

`python bin/languages/analysis/analysis.py --setup experiment_setups/final.json --model_size 4 --max_quantifier_length 4 --name natural_gradual --comp_strat wordcomplexity --inf_strat simmax --pareto evolutionary --table_name main_data`

# TODOs

* Experiment setups
    - incorporate into the setup instead of command-line: max quantifier length, model size, comp strat, inf strat
    - move from json to yaml?
* General cleaning: