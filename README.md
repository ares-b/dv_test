# Instructions
You need to flatten the attached tree ( tree_to_convert.txt ) into a set of strategies.

A strategy is a combination of :

- a strategy definition : a sequence of conditions of the form "{feature} = {value}" or
"{feature} != {value}" separated with "and" operators only.
    - e.g : "phone=12 & language=2 & size!=300x600"
- a leaf value

The syntax of a strategy is given by {strategy definition}:{leaf_value}.

# Modalities
- Your script should be coded in Python
- You have to code a function which takes the tree_to_convert.txt file as input, flattens
it, and writes the output strategies into another strategies.txt file.
- Your function needs to be generic. It could take as input any tree of the same
structure. You can assume similar tree will have :
    - only OR conditions
    - only = != operators
    - various variables names (only letters) and tree depth
- Your script shouldn’t return impossible strategies:
    - "phone=5 & phone=7" is not allowed
- Your script should simplify strategies when possible :
    - "value=4" is better than "value!=3 & value=4"
- The operator "&" is the only operator allowed in a strategy

# Example

Leaf 4 translates into the following strategy : 
"device_type!=pc & browser!=7 & browser=8 : 0.000881108"\
Which is then simplified in : "device_type!=pc & browser=8 : 0.000881108"
