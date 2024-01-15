# IFIS (*Interval-Valued Inference System based on Simpful*)
The motivation for creating a library for the application of interval-valued fuzzy inference was the fact that methods for classifying uncertain data are important in many applications.

The Interval-Valued Inference System (IFIS) is implemented in the Python 3 programming language. It is an extension of the Simpful library [1] and its dependencies are Numpy and Scipy. The latest version of IFIS currently supports the following features:
1. Definition of polygonal (e.g., vertex-based) and functional (e.g., sigmoidal, Gaussian, custom shaped) membership functions.
2. Definition of interval-valued fuzzy rules as strings of text written in natural language.
3. Definition of arbitrarily complex fuzzy rules built with the logic operators AND, OR (suitable interval-valued fuzzy operations built from minimum and maximum, respectively) or NOT (interval fuzzy negation), or arbitrary interval-valued aggregations.
4. Mamdani and Takagi–Sugeno inference methods.

Given values for the antecedents as input, IFIS can perform interval-valued fuzzy inference and provide the final output values.

The elements of our system are described below:

I. *Preparation of data – 2-fuzzification*. Defining the interval fuzzy sets that will subsequently be linked with linguistic variables

Data preparation takes place via the following two paths:

a. The data are input as real values. Then the interval-valued fuzzy set is defined by the membership function that describes it. Within the library, standard types of membership functions are defined, e.g. triangular, trapezoidal, sigmoidal, Gaussian, etc. It is also possible to define membership functions based on a specified function or by specifying characteristic points of that function. To define interval-valued fuzzy sets, it is required to provide two features of the membership function, describing, respectively, the beginning and the end of the interval set onto.

b. The data are input as real value intervals. Then it is possible to describe a fuzzy set with one membership function.

The interval data obtained for both paths will satisfy the assumption:

{[a1, a2]:  a1 <= a2,  a1, a2 belongs to [0.1]}.

II. *Inference Process. Rules*

The construction of an inference system based on the interval extension of the Simpful library consists in:

a. Defining the parameters of interval-valued fuzzy sets (parameter functions built as objects of an abstract class, extending the FuzzySet object) linked to linguistic variables. Moreover, we give the boundaries of the universe for each variable/attribute (except when building a function based on points, where the minimum and maximum values determine the limit values) to facilitate their graphic representation.

b. Determining interval linguistic variables based on the defined interval-valued fuzzy sets – creating objects by extending LinguisticVariable objects. Depending on the selected inference type (Mamdani or Takagi–Sugeno), an appropriate representation of the inferring system output is defined.

c. Providing a set of inference rules based on the defined interval linguistic variables and fuzzy sets. As part of the rules for premises and output values, you can use the logical operators AND, OR, NOT, and chosen interval-valued aggregation functions, which are also specified in interval form.

d. Launching the inference process according to the defined types (Mamdani or Takagi–Sugeno) with given values of the variables. For the Takagi–Sugeno system, we also need to define the output functions, along with their identification for rule definitions.

e. The inference results take into account the appropriate defuzzification method: centroid (Mamdani) or weighted mean (Takagi–Sugeno), and any decision thresholds.

## Installation
To be able to use our library you need to download its sources. Earlier you must install the Simpful library from https://github.com/aresio/simpful

## Citing IFIS
If you find IFIS useful for your research, please cite our work as follows:

[1] Spolaor S., Fuchs C., Cazzaniga P., Kaymak U., Besozzi D., Nobile M.S.: Simpful: a user-friendly Python library for 
fuzzy logic, International Journal of Computational Intelligence Systems, 13(1):1687–1698, 2020 [DOI:10.2991/ijcis.d.201012.002].

[2] Grochowalski P.,  Kosior D., Gil D., Kozioł W., Pękala B., Dyczkowski K., Python library for interval-valued fuzzy inference, to appear.

## Illustrative examples
In this section, we provide example of practical applications, together with their corresponding Python code, to demonstrate the potential and the use of IFIS. They involve the definition of a Mamdani and Takagi–Sugeno IFIS  for the tipping problem.

### Tipping problem
The tipping problem consists in computing a fair tip (in terms of a percentage of the overall bill), taking into account a restaurant’s services. Listing 1 shows an example of IFIS code defining an interval inference system that calculates the amount of the tip on the basis of two input variables, describing food quality and service quality.

Listing 1 illustrates a range inference system whose task is to determine the value of the tip for the waiter (as a percentage of the total order value) based on the evaluation of the service in an example restaurant. To determine the size of the tip, two inputs are taken into account: food quality and service quality. The example illustrates how to define an inference system based on interval fuzzy sets. The basis for the newly created library, which has already been mentioned, is the Simpful library, which supports the creation of fuzzy inference systems.

An example implementation of an inference system based on the Takagi–Sugeno method:

```
from simpful import *
from interval_simpful.interval_fuzzy_sets import *
from interval_simpful.interval_fuzzy_system import *
from interval_simpful.interval_linguistic_variable import *

# A simple interval fuzzy inference system for the tipping problem
# Create interval fuzzy system object
iFS = IntervalFuzzySystem()

# Define interval fuzzy sets and interval linguistic variables
S_1 = IntervalFuzzySet(function_start=Triangular_MF(a=0, b=0, c=5), function_end=Trapezoidal_MF(a=1, b=1, c=1, d=6), term='poor')
S_2 = IntervalFuzzySet(function_start=Triangular_MF(a=0, b=5, c=10), function_end=Trapezoidal_MF(a=0, b=4, c=6, d=10), term='good')
S_3 = IntervalFuzzySet(function_start=Triangular_MF(a=5, b=10, c=10), function_end=Trapezoidal_MF(a=4, b=9, c=10, d=10), term='excellent')
iFS.add_linguistic_variable("Service", IntervalLinguisticVariable([S_1, S_2, S_3], concept="Service quality", universe_of_discourse=[0, 10]))

F_1 = IntervalFuzzySet(function_start=Triangular_MF(a=0, b=0, c=8), function_end=Trapezoidal_MF(a=1, b=1, c=2, d=10), term='rancid')
F_2 = IntervalFuzzySet(function_start=Triangular_MF(a=2, b=10, c=10), function_end=Trapezoidal_MF(a=0, b=8, c=10, d=10), term='delicious')
iFS.add_linguistic_variable("Food", IntervalLinguisticVariable([F_1, F_2], concept="Food quality", universe_of_discourse=[0, 10]))

# Define output crisp values
iFS.set_crisp_output_value("small", 5)
iFS.set_crisp_output_value("average", 15)

# Define function for generous tip (food score + service score + 5%)
iFS.set_output_function("generous", "Food+Service+5")

# Define fuzzy rules
R1 = "IF (Service IS poor) OR (Food IS rancid) THEN (Tip IS small)"
R2 = "IF (Service IS good) THEN (Tip IS average)"
R3 = "IF (Service IS excellent) OR (Food IS delicious) THEN (Tip IS generous)"
iFS.add_rules([R1, R2, R3])

# Set antecedents values
iFS.set_variable("Service", 4)
iFS.set_variable("Food", 8)

# Perform Sugeno interval inference and print output
print(iFS.Sugeno_interval_inference(["Tip"]))
```

In the first step, on line 8, a root object is created representing the inference system based on interval fuzzy sets. The resources of this object will be supplemented with individual elements of the system enabling the implementation of fuzzy inference. In lines 11–18, interval fuzzy sets are created and linked to the appropriate interval linguistic variables. Each of the interval fuzzy sets (in the current version of the library) is described by two membership functions, one for the beginning of the interval and the other for its end. These functions can be defined by means of defined functions that represent typical membership functions, e.g. triangular, trapezoidal, etc. (taken from the Simpful library), by means of characteristic points that define them or through their own function definitions. In the example considered, two input data (input linguistic variables) are considered: Service quality and Food quality. Service quality is described by three compartments (fuzzy harvests), “poor”, “good” and “excellent”, and Food quality by two fuzzy harvests, “rancid” and “delicious”.

In lines 21–25, the output of the inferring system is defined, the implementation of which depends on the selected inference method. In the inference system based on the Mamdani method, the output is defined in the form of an interval fuzzy set, whereas with the Takagi–Sugeno inference method, specific output functions are defined. In the example under consideration, two exact output values are given, corresponding to tip values of 5% and 15% of the order value, and one value which is derived from the relationship specified in line 25. Lines 27–30 define the fuzzy inference rules, and lines 33–34 determine the real values of the input variables (two variables in this example). The entire inference process starts on line 38, using the Takagi–Sugeno method of inference. For the example input data, the rating for service quality is equal to 4 and the rating for food quality is equal to 8 (for limits [0,10]), and the result is a tip value defined by the range [14.1667%, 14.78143%]. This specifies the range within which the tip value may vary as a percentage of the total order value.

## Further info
If you need further information, please write an e-mail to: pgrochowalski@ur.edu.pl

### References
[1] Spolaor S., Fuchs C., Cazzaniga P., Kaymak U., Besozzi D., Nobile M.S.: Simpful: a user-friendly Python library 
for fuzzy logic, International Journal of Computational Intelligence Systems, 13(1):1687–1698, 2020 
[DOI:10.2991/ijcis.d.201012.002]

[2] Grochowalski P.,  Kosior D., Gil D., Kozioł W., Pękala B., Dyczkowski K., Python library for interval-valued fuzzy 
inference, to appear

