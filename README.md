# formalmath

A formal mathematics package.

## setmm

A port for [metamath](https://us.metamath.org) and `set.mm`. The language `metamath` is a math proof verifying language. And, `set.mm` is its main database of theorems, based on the classical ZFC axiom system.

`MObject` is the basic class. Any `MObject` have a label. Some of them have short_code or metamath_code. The label system is unique (if you create a new MObject with the same label with existing one, the program will raise ValueError). So does the short_code and metamath_code.

 `Constant` is the class of constants, corresponding to $c statements in metamath.

`Variable` is the class of variables, corresponding to $v statements in metamath.

`Formula` is the base class of formulas, corresponding to wff in metamath and set.mm.

`FormulaVariable` is the class of formula with only one symbol.

`FormulaTemplate` is the class of templates that generate new formula out of old formulas and other symbols.

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
```

