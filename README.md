
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


#### generate individual quantifiers

`python bin/individual_quantifiers/generate.py --setup experiment_setups/final.json`


#### measure properties of them

`python bin/individual_quantifiers/measure_expression_complexity.py --setup experiment_setups/final.json`

`python bin/individual_quantifiers/measure_expression_monotonicity.py --setup experiment_setups/final.json`

`python bin/individual_quantifiers/measure_expression_conservativity.py --setup experiment_setups/final.json`


#### generate pseudo-natural quantifiers

`python bin/individual_quantifiers/generate_natural_expressions.py --setup experiment_setups/final.json`


#### run evolutionary algorithm to estimate pareto frontier

`python bin/languages/generate_evolutionary.py --setup=experiment_setups/final.json --lang_size 10 --sample_size 2000 --generations 100 --max_mutations 3`


#### generate languages with varying degrees of naturalness

`python bin/languages/sample_indexset_degrees.py --setup experiment_setups/final.json --indices natural --sample 8000`

#### generate "random" languages
`python bin/languages/languages.py --setup experiment_setups/final.json --sample 2000`


#### measure complexity and informativeness

`python bin/languages/measure.py --setup experiment_setups/final.json --name natural_gradual`
`python bin/languages/measure.py --setup experiment_setups/final.json --name random`

#### measure monotonicity and conservativity

`python bin/languages/measure_monotonicity.py --setup experiment_setups/final.json --name natural_gradual`
`python bin/languages/measure_monotonicity.py --setup experiment_setups/final.json --name random`

`python bin/languages/measure_conservativity.py --setup experiment_setups/final.json --name natural_gradual`
`python bin/languages/measure_conservativity.py --setup experiment_setups/final.json --name random`


#### analysis

`python bin/languages/analysis/estimate_pareto.py --setup experiment_setups/final.json`
`python bin/languages/analysis/analyze.py --setup experiment_setups/final.json`

# TODOs

* Experiment setups: move from json to yaml?
* General cleaning:
* Finalize `siminf` as actual package