# formalmath

A formal mathematics package.

## Install

```
pip install formalmath
```

## setmm

A port for [metamath](https://us.metamath.org) and `set.mm`. The language `metamath` is a math proof verifying language. And, `set.mm` is its main database of theorems, based on the classical ZFC axiom system.

`MObject` is the basic type Any `MObject` have a label. Some of them have short_code or metamath_code. The label system is unique (if you create a new MObject with the same label with existing one, the program will raise ValueError). So does the short_code and metamath_code.

 `Constant` is the type of constants, corresponding to $c statements in metamath.

`Variable` is the type of variables, corresponding to $v statements in metamath.

`Formula` is the base type of formulas, corresponding to wff in metamath and set.mm.

`FormulaConstant` are Constant objects that are also Formulas.

`FormulaVariable` are Variable objects that are also Formulas.

`ClassType` is the base type of classes, corresponding to class in metamath and set.mm.

`ClassConstant` are Constant objects that are also `ClassType` objects.

`ClassVariable` are Variable objects that are also `ClassType` objects.

`Template` are base type of templates. A template can generate new formula or class out of old.

`FormulaTemplate` denote templates that generate new formula out of old formulas and other symbols.

`ClassTemplate` denote templates that generate new `ClassType` objects out of old `ClassType` objects and other symbols.

`SetVariable` denote `setvar` notation in metamath and set.mm.

The port of other concepts in metamath and set.mm is a work in process.

Example code:

```python
from formalmath.setmm import *
test1 = MObject("x1")
test2 = MObject("y1")
# test3 = MObject("x1")
print(test1) # output: MObject("x1")
test3 = MObject.find_MObject_by_label("y1")
print(test3) # output: MObject("y1")

lp1 = Constant("\\left(")
rp1 = Constant("\\right)")
# lp2 = Constant("\\left(")
print(lp1) # output: Constant("\left(")
testConst = Constant.find_MObject_by_label("\\right)")
print(testConst) # output: Constant("\right)")

lp = Constant("(")
rp = Constant(")")
ra = Constant("->")
phi = FormulaVariable("phi")
psi = FormulaVariable("psi")
chi = FormulaVariable("chi")
phi_implies_psi = Formula("phips",list_of_symbols=[lp,phi,ra,psi,rp])
complex_imply = Formula("ccimply",list_of_symbols=[lp,phi_implies_psi,ra,chi,rp])
print(complex_imply) # Formula("( ( phi -> psi ) -> chi )")
wi = FormulaTemplate({"var_types":{"x":Formula,"y":Formula},"template":[lp,"x",ra,"y",rp]})
print(wi)
# Template:  (  x  ->  y  )
# Types:
# x : Formula
# y : Formula
nf = wi.generate({"x":psi,"y":chi})
print(nf) # Formula("( psi -> chi )")
nf2 = wi.generate({"x":phi,"y":nf})
nf3 = wi.generate({"x":nf,"y":nf2})
print(nf3) # Formula("( ( psi -> chi ) -> ( phi -> ( psi -> chi ) ) )")

wi2 = wi.generate_template({"x":"y","y":"z"})
wiwi = wi.generate_template({"x":wi,"y":wi2})
print(wiwi)
# Template:  (  (  x  ->  y  )  ->  (  y  ->  z  )  )
# Types:
# x : Formula
# y : Formula
# z : Formula
wi3 = wiwi.generate_template({"x":wi2,"y":wiwi,"z":"w"})
print(wi3)
# Template:  (  (  (  y  ->  z  )  ->  (  (  x  ->  y  )  ->  (  y  ->  z  )  )  ) 
#  ->  (  (  (  x  ->  y  )  ->  (  y  ->  z  )  )  ->  w  )  )
# Types:
# y : Formula
# z : Formula
# x : Formula
# w : Formula
one = ClassConstant("1")
two = ClassConstant("2")
three = ClassConstant("3")
equal = Constant("=")
plus = Constant("+")
temp_plus = ClassTemplate({"var_types":{"a":ClassType,"b":ClassType},"template":["a",plus,"b"]})
temp_eq = FormulaTemplate({"var_types":{"u":ClassType,"v":ClassType},"template":["u",equal,"v"]})
temp_new = temp_eq.generate_template({"u":temp_plus,"v":"c"})
print(temp_new)
# Template:  a  +  b  =  c
# Types:
# a : ClassType
# b : ClassType
# c : ClassType
eq1p2e3 = temp_new.generate({"a":one,"b":two,"c":three})
print(eq1p2e3) # Formula("1 + 2 = 3")
```

