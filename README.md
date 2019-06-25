
# Simplicity vs. Informativeness trade-off for quantifiers

This code accompanies my Master's thesis 'The influence of the simplicity/informativeness trade-off on the semantic typology of quantifiers' for the MSc Logic at the University of Amsterdam.

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

Python 3.5. Get the required packages by running `pip install`.

## Running the code

Almost all code requires three main parameters:

- A path to the _Experiment Setup_ (see the folder ExperimentSetups). This specifies the grammar, using operators from [`Operator.py`](Code/Operator.py)
- The model size
- The maximum quantifier length

This will put the results of said code in results/[ExperimentSetupName]\_length=[length]\_size=[size]

### Generation

[`generate.py`](Code/IndividualQuantifiers/generate.py) is used to generate expressions.

[`merge_presuppositions.py`](Code/IndividualQuantifiers/merge_presuppositions.py) is used to combine these into presuppositions. This requires expressions.

[`languages.py`](Code/Languages/languages.py) is used to sample languages. This requires expressions.

[`generate_evolutionary.py`](Code/Languages/generate_evolutionary.py`) is used to approximate the Pareto Front using an evolutionary algorithm. This requires expressions and their complexities.

### Measuring expressions

Expressions are measured using the `Code/IndividualQuantifiers/measure_expression_*.py` files. This saves the results in a separate file.

### Measuring presuppositions
The simplicity and informativeness of quantifiers with presuppositions are measured using [`measure.py`](Code/IndividualQuantifiers/measure.py). 

### Measuring languages
Languages are measured using the `Code/IndividualQuantifiers/measure_*.py` files. Most require the expressions to be measured first (e.g. to measure the monotonicity of languages one first needs to measure the monotonicity of expressions).

## Running the experiments

### Individual Quantifiers

```
Code/IndividualQuantifiers/generate.py ExperimentSetups/Logical.json 12 10
Code/IndividualQuantfiers/measure_expression_complexity.py ExperimentSetups/Logical.json 12 10 
Code/IndividualQuantifiers/measure_expression_informativeness.py ExperimentSetups/Logical.json 12 10
Code/IndividualQuantifiers/Analysis/plot_expressions.py ExperimentSetups/Logical.json 12 10
```

### Presuppositions
```
Code/IndividualQuantifiers/generate.py ExperimentSetups/Logical.json 7 10
Code/IndividualQuantifiers/merge_presuppositions.py ExperimentSetups/Logical.json 7 10
Code/IndividualQuantifiers/measure.py ExperimentSetups/Logical.json 7 10
```

### Languages setup
```
# Generate the expressions and measure them
Code/IndividualQuantifiers/generate.py ExperimentSetups/Final.json 12 10
Code/IndividualQuantfiers/measure_expression_complexity.py ExperimentSetups/Final.json 12 10 
Code/IndividualQuantifiers/measure_expression_monotonicity.py ExperimentSetups/Final.json 12 10
Code/IndividualQuantifiers/measure_expression_conservativity.py ExperimentSetups/Final.json 12 10
Code/IndividualQuantifiers/generate_natural_expressions.py ExperimentSetups/Final.json 12 10

# Generate using evolutionary algorithm: 2000 samples, 100 generations
Code/Languages/generate_evolutionary ExperimentSetups/Final.json 12 10 10 2000 100 -m 3 --name=evolutionary

```

### Languages: Experiment 1
```
# Sample the quasi-natural languages
Code/Languages/Languages.py --indices=natural ExperimentSetups/Final.json 12 10 10 --sample=2000 --name=natural_2000
Code/Languages/measure.py ExperimentSetups/Final.json 12 10 10 --name=natural_2000 wordcomplexity simmax

# Sample random languages
Code/Languages/Languages.py ExperimentSetups/Final.json 12 10 10 --sample=2000 --name=regular_2000
Code/Languages/measure.py ExperimentSetups/Final.json 12 10 10 --name=regular_2000 wordcomplexity simmax

# Measure optimality and compose into pandas table
Code/Languages/Analysis/measure_moo_performance.py ExperimentSetups/Final.json 12 10 exp1 evolutionary_2000 natural_2000 regular_2000
```

This yields the pandas table `exp1.csv`

### Languages: Experiment 2
```
# Sample languages with a uniform distribution over naturalness
Code/Languages/sample_indexset_degrees.py ExperimentSetups/Final.json 12 10 natural 10 8000 --name=natural_gradual_2000

# Measure the various properties
Code/Languages/measure.py ExperimentSetups/Final.json 12 10 10 --name=natural_gradual_2000 wordcomplexity simmax
Code/Languages/measure_monotonicity.py ExperimentSetups/Final.json 12 10 10 --name=natural_gradual_2000
Code/Languages/measure_conservativity.py ExperimentSetups/Final.json 12 10 10 --name=natural_gradual_2000

# Measure optimality and compose into pandas table
Code/Languages/Analysis/measure_moo_performance.py ExperimentSetups/Final.json 12 10 exp2 evolutionary_2000 natural_gradual_2000
```

This yields the pandas table `exp2.csv`

