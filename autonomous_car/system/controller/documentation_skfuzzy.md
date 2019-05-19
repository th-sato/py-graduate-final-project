## Documentação do Skfuzzy
As informações aqui apresentadas foram obtidas do seguinte [link.](https://pythonhosted.org/scikit-fuzzy/api/api.html)

###### skfuzzy.control.Antecedent(universe, label) [Link](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.control.html#antecedent)
Antecedent (input/sensor) variable for a fuzzy control system.
* **universe:** Universe variable. Must be 1-dimensional and convertible to a NumPy array.
* **label:** Name of the universe variable.

###### skfuzzy.control.Consequent(universe, label) [Link](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.control.html#consequent)
Consequent (output/control) variable for a fuzzy control system.
* **universe:** Universe variable. Must be 1-dimensional and convertible to a NumPy array.
* **label:** Name of the universe variable.

###### skfuzzy.control.Rule(antecedent=None, consequent=None, label=None) [Link](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.control.html#rule)
Rule in a fuzzy control system, connecting antecedent(s) to consequent(s).
* **antecedent:** Antecedent terms serving as inputs to this rule. Multiple terms may be combined using operators | (OR), & (AND), ~ (NOT), and parentheticals to group terms.
* **consequent:** Consequent terms serving as outputs from this rule. Multiple terms may be combined using operators | (OR), & (AND), ~ (NOT), and parentheticals to group terms.
* **label:** Label to reference the meaning of this rule. Optional, but recommended. If provided, the label must be unique among rules in any particular ControlSystem.

###### skfuzzy.control.ControlSystem(rules=None) [Link](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.control.html#controlsystem)
Base class to contain a Fuzzy Control System.
* **rules:** Rule or iterable of Rules, optional. If provided, the system is initialized and populated with a set of fuzzy Rules (see skfuzzy.control.Rule). This is optional. If omitted the ControlSystem can be built interactively.

###### skfuzzy.control.ControlSystemSimulation(control_system, clip_to_bounds=True, cache=True, flush_after_run=1000) [Link](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.control.html#controlsystemsimulation)
Calculate results from a ControlSystem.
* **control_system:** A fuzzy ControlSystem object.
* **clip_to_bounds:** Controls if input values should be clipped to the consequent universe range. Default is True.
* **cache:** Controls if results should be stored for reference in fuzzy variable objects, allowing fast lookup for repeated runs of .compute(). Unless you are heavily memory constrained leave this True (default). 
* **flush_after_run:** Clears cached results after this many repeated, unique simulations. The default of 1000 is appropriate for most hardware, but for small embedded systems this can be lowered as appropriate. Higher memory systems may see better performance with a higher limit.

###### skfuzzy.pimf(x, a, b, c, d) [Link](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.html#pimf)
Pi-function fuzzy membership generator.
* **x:** Independent variable.
* **a:** Left ‘foot’, where the function begins to climb from zero.
* **b:** Left ‘ceiling’, where the function levels off at 1.
* **c:** Right ‘ceiling’, where the function begins falling from 1.
* **d:** Right ‘foot’, where the function reattains zero.

###### skfuzzy.trimf(x, abc) [Link](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.html#trimf)
Triangular membership function generator.
* **x:** Independent variable.
* **abc:** Three-element vector controlling shape of triangular function. Requires a <= b <= c.


###### skfuzzy.control.ControlSystemSimulation.compute() [Link](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.control.html#controlsystemsimulation)
Compute the fuzzy system.

###### skfuzzy.control.ControlSystemSimulation.compute_rule(rule) [Link](https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.control.html#controlsystemsimulation)

Implement rule according to Mamdani inference.

The three step method consists of:
* Aggregation
* Activation
* Accumulation