'''
Python port for a slightly extended version of the formal language metamath (us.metamath.org) and the theorem database set.mm written by metamath. This system includes over 40000 theorems in the classic ZFC axiom system.

The basic classes will be defined in this file. That includes:
0. MObject. The base class for all classes.
1. Constant. That correspond to $c statement in metamath.
2. Variable. That correspond to $v statement in metamath.
3. FormulaTemplate. That correspond to $a statements starting with wff symbol. Basically, it generates new formula from old. But the template's symbol list can also have Constant, ClassVariable, ClassType, SetVariable, etc.
4. Formula. That correspond to wff in metamath and set.mm. It is not a part of the basic metamath language. But it is defined in set.mm to denote well formed formula. There is always new ways to form a wff, when a new term is introduced. But all of them correspond to a conbination of old terms.
5. ClassType. That correspond to class in metamath and set.mm.
6. ClassVariable. That correspond to class denoted by a single symbol in metamath and set.mm.
7. SetVariable. That correspond to setvar in metamath and set.mm.
8. Axiom. That correspond to $a statements that are axioms.
9. Definition. That correspond to $a statements that are definitions.

Inherit relation:
MObject ----- Constant
          |
          |-- Variable -- SetVariable
          |         
          |-- Formula -- FormulaVariable (also inherit Variable)
          |
          |-- FormulaTemplate
          |
          |-- ClassType -- ClassVariable (also inherit Variable)

Some basic constants will be defined here too, such as left and right parenthesis, well-formed formula symbol and turnstile.
'''

class MObject:
    '''
    Base class for all metamath classes.
    Use this to ensure the uniqueness of labels and codes.
    '''

    # global dictionaries that ensures the uniqueness of MObject labels, latex_codes and metamath_codes.
    # these dicts can also be used to search MObjects by labels, latex_codes and metamath_codes.
    MObject_labels = {}
    MObject_latex_codes = {}
    MObject_metamath_codes = {}

    def __init__(self, label=None, latex_code=None, metamath_code=None):
        '''
        construction function of MObject.
        label: label of the MObject. It is unique.
        latex_code: a latex code for the MObject. Also unique.
        metamath_code: the corresponding original code in set.mm.
        '''
        if label:
            # ensure the uniqueness of label
            self._check_unique_label(label)
            # define the label of an MObject
            self.label = label
        
        if latex_code:
            # ensure the uniqueness of latex_code
            self._check_unique_latex_code(latex_code)
            # define the latex_code of an MObject
            self.latex_code = latex_code

        if metamath_code:
            # ensure the uniqueness of metamath_code
            self._check_unique_metamath_code(metamath_code)
            # define the metamath_code of an MObject
            self.metamath_code = metamath_code

        # add the new MObject into dicts
        MObject.MObject_labels[label] = self
        if latex_code:
            MObject.MObject_latex_codes[latex_code] = self
        if metamath_code:
            MObject.MObject_metamath_codes[metamath_code] = self
    
    def _check_unique_label(self, label):
        '''
        ensure label is not seen in MObject_labels
        '''
        # if label is used before, raise ValueError.
        if label in MObject.MObject_labels:
            raise ValueError("Duplicate label: {}".format(label))
        
    def _check_unique_latex_code(self, latex_code):
        '''
        ensure latex_code is not seen in MObject_latex_codes
        '''
        # if latex_code is used before, raise ValueError.
        if latex_code in MObject.MObject_latex_codes:
            raise ValueError("Duplicate latex_code: {}".format(latex_code))

    def _check_unique_metamath_code(self, metamath_code):
        '''
        ensure metamath_code is not seen in MObject_metamath_codes
        '''
        # if metamath_code is used before, raise ValueError.
        if metamath_code in MObject.MObject_metamath_codes:
            raise ValueError("Duplicate metamath_code: {}".format(metamath_code))
    
    def __str__(self):
        '''
        print MObject
        '''
        return f"MObject(\"{self.label}\")"
    
    @classmethod
    def find_MObject_by_label(cls, label):
        '''
        Find MObject by label. Need exact match. 
        '''
        if label in MObject.MObject_labels:
            return MObject.MObject_labels[label]
        else:
            raise ValueError("MObject label not found: {}".format(label))

    @classmethod
    def find_MObject_by_latex_code(cls, latex_code):
        '''
        Find MObject by latex_code. Need exact match. 
        '''
        if latex_code in MObject.MObject_latex_codes:
            return MObject.MObject_latex_codes[latex_code]
        else:
            raise ValueError("MObject latex_code not found: {}".format(latex_code))

    @classmethod
    def find_MObject_by_metamath_code(cls, metamath_code):
        '''
        Find MObject by metamath_code. Need exact match. 
        '''
        if metamath_code in MObject.MObject_metamath_codes:
            return MObject.MObject_metamath_codes[metamath_code]
        else:
            raise ValueError("MObject metamath_code not found: {}".format(metamath_code))

class Constant(MObject):
    '''
    $c statement in metamath, denote constant objects.
    Example: left and right parenthesis, wff symbol
    '''
    def __init__(self, label=None, latex_code=None, metamath_code=None):
        '''
        construction function of Constant.
        just need to inherit from MObject.
        '''
        super().__init__(label, latex_code, metamath_code)
    
    def __str__(self):
        '''
        print Constant. will override the __str__ method in MObject.
        '''
        return f"Constant(\"{self.label}\")"

class Variable(MObject):
    '''
    $v statement in metamath, denote variable objects.
    '''
    def __init__(self, label=None, latex_code=None, metamath_code=None):
        '''
        construction function of Variable.
        just need to inherit from MObject.
        '''
        super().__init__(label, latex_code, metamath_code)
    
    def __str__(self):
        '''
        print Variable. will override the __str__ method in MObject.
        '''
        return f"Variable(\"{self.label}\")"

class Formula(MObject):
    '''
    base class for well formed formulas.
    '''
    def __init__(self, label=None, latex_code=None, metamath_code=None, list_of_symbols=None):
        '''
        construction function for Formula.
        list_of_symbols: a list of constants and formulas and classes and setvars, making the symbols of the new formula 
        '''
        super().__init__(label, latex_code, metamath_code)
        if list_of_symbols:
            self._check_symbol_type(list_of_symbols)
            my_list = []
            for symbol in list_of_symbols:
                if isinstance(symbol, (Formula, ClassType)):
                    my_list = my_list + symbol.list_of_symbols
                else:
                    my_list.append(symbol)
            self.list_of_symbols = my_list
    
    def _check_symbol_type(self, list_of_symbols):
        '''
        Ensure that all symbols in the list_of_symbols are of type Constant, Formula ClassType and SetVariable.
        Otherwise, raise TypeError.
        '''
        for symbol in list_of_symbols:
            if not isinstance(symbol, (Constant, Formula, ClassType, SetVariable)):
                raise TypeError(f"{symbol}: not in supported type. We support Constant, Formula, ClassType and SetVariable for symbols in list_of_symbols.")
    
    def __str__(self):
        '''
        print Formula. will override the __str__ method in MObject.
        '''
        labelstr = ' '.join([f"{s.label}" for s in self.list_of_symbols])
        return f"Formula(\"{labelstr}\")"
    
class FormulaVariable(Variable, Formula):
    '''
    $f statement of form $f wff varname $. It means that varname represents a well formed formula.
    This class is the special kind of Formula consisting of only one variable.
    '''
    def __init__(self, label=None, latex_code=None, metamath_code=None):
        super().__init__(label, latex_code, metamath_code)
        self.list_of_symbols = [self]
    
    def __str__(self):
        return f"Formula(\"{self.label}\")"

class ClassType(MObject):
    '''
    base class for classes of set.mm.
    '''
    def __init__(self, label=None, latex_code=None, metamath_code=None, list_of_symbols=None):
        '''
        construction function for ClassType.
        list_of_symbols: a list of constants and formulas and classes and setvars, making the symbols of the new class
        '''
        super().__init__(label, latex_code, metamath_code)
        if list_of_symbols:
            self._check_symbol_type(list_of_symbols)
            my_list = []
            for symbol in list_of_symbols:
                if isinstance(symbol, (Formula, ClassType)):
                    my_list = my_list + symbol.list_of_symbols
                else:
                    my_list.append(symbol)
            self.list_of_symbols = my_list
    
    def _check_symbol_type(self, list_of_symbols):
        '''
        Ensure that all symbols in the list_of_symbols are of type Constant, Formula, ClassType and SetVariable.
        Otherwise, raise TypeError.
        '''
        for symbol in list_of_symbols:
            if not isinstance(symbol, (Constant, Formula, ClassType, SetVariable)):
                raise TypeError(f"{symbol}: not in supported type. We support Constant, Formula, ClassType and SetVariable for symbols in list_of_symbols.")
    
    def __str__(self):
        '''
        print ClaaType. will override the __str__ method in MObject.
        '''
        labelstr = ' '.join([f"{s.label}" for s in self.list_of_symbols])
        return f"Formula(\"{labelstr}\")"

class ClassVariable(Variable, ClassType):
    '''
    $f statement of form $f class varname $. It means that varname represents a class.
    '''
    def __init__(self, label=None, latex_code=None, metamath_code=None):
        super().__init__(label, latex_code, metamath_code)
        self.list_of_symbols = [self]
    
    def __str__(self):
        return f"ClassVariable(\"{self.label}\")"

class SetVariable(Variable):
    '''
    $f statement of form $f setvar varname $. It means that varname represents a set variable.
    '''
    def __init__(self, label=None, latex_code=None, metamath_code=None):
        super().__init__(label, latex_code, metamath_code)
    
    def __str__(self):
        return f"SetVariable(\"{self.label}\")"

class FormulaTemplate(MObject):
    '''
    $a statements that generates new Formula from old by substitution.
    '''
    def __init__(self, template=None, label=None, latex_code=None, metamath_code=None):
        '''
        template: a dictionary that has keys "var_types" and "template"
        example: {"var_types":{"x":Formula,"y":Formula},"template":[lp,"x",ra,"y",rp]}
        this example means in the Template of Formula "( x -> y )", x, y should be replaced with Formulas.
        '''
        super().__init__(label, latex_code, metamath_code)
        # check that the template has the right format.
        self._check_template(template)            
        setattr(self, "template", template)
        
    def generate(self, vars, mylabel=None, mycode=None, mymmcode=None):
        '''
        use the template to define a generator of new Formula from old
        '''
        mylist = []
        for symbol in self.template["template"]:
            if isinstance(symbol,str):
                if self.template["var_types"][symbol] in [Formula,ClassType]:
                    if len(vars[symbol].list_of_symbols) > 1:
                        mylist = mylist + vars[symbol].list_of_symbols
                    else:
                        mylist.append(vars[symbol])
                else:
                    mylist.append(vars[symbol])
            else:
                mylist.append(symbol)
        newFormula = Formula(mylabel,mycode,mymmcode,mylist)
        return newFormula
    
    def generate_template(self, vars, mylabel=None, mycode=None, mymmcode=None):
        '''
        use the template to define a generator of new FormulaTemplate from old 
        '''
        new_var_types = {}
        new_template = []
        var_types = self.template["var_types"]
        temp = self.template["template"]

        # example 1. temp is (x->y), var_types={"x":Formula,"y":Formula}, vars={"x":"z","y":"w"}
        # then new_var_types should be {"z":Formula,"w":Formula}
        # and, new_template should be (z->w)

        # example 2. temp is (x->y), var_types={"x":Formula,"y":Formula}, vars={"x":f1,"y":f2}
        # where f1 is a template: temp is (z->w), var_types={"z":Formula,"w":Formula},
        # f2 is also a template: temp is (z->t), var_types={"z":Formula,"t":Formula},
        # then new_var_types should be {"z":Formula,"w":Formula,"t":Formula}
        # and, new_template should be ((z->w)->(z->t))

        for item in vars.keys():
            if isinstance(vars[item], str):
                if vars[item] not in new_var_types.keys():
                    new_var_types[vars[item]] = var_types[item]
                else:
                    if new_var_types[vars[item]] != var_types[item]:
                        raise ValueError(f"Conflict types: {new_var_types[vars[item]]} and {var_types[item]}")
            elif isinstance(vars[item], FormulaTemplate):
                for symbol in vars[item].template["var_types"].keys():
                    if symbol not in new_var_types.keys():
                        new_var_types[symbol] = vars[item].template["var_types"][symbol]
                    else:
                        if new_var_types[symbol] != vars[item].template["var_types"][symbol]:
                            raise ValueError(f"Conflict types: {new_var_types[symbol]} and {vars[item].template['var_types'][symbol]}")
            else:
                pass
        
        for symbol in temp:
            if isinstance(symbol, str):
                if isinstance(vars[symbol],str):
                    new_template.append(vars[symbol])
                else:
                    if symbol not in vars.keys():
                        raise ValueError(f"Undefined symbol : {symbol}")
                    if not isinstance(vars[symbol],FormulaTemplate):
                        raise ValueError(f"Unsupported type : {vars[symbol]}")
                    new_template = new_template + vars[symbol].template["template"]
            else:
                new_template.append(symbol)
        
        new_formula_temp = FormulaTemplate({"var_types":new_var_types,"template":new_template},mylabel,mycode,mymmcode)
        return new_formula_temp

    def _check_template(self, template):
        '''
        check that the template has the right format.
        '''
        if not isinstance(template["template"], list):
            raise ValueError(f"Template is not a list.")
        vars = template["var_types"].keys()
        for symbol in template["template"]:
            if not isinstance(symbol, Constant):
                # ensure the variable symbols in the template has not appeared in the labels of MObjects defined before 
                self._check_unique_label(symbol)
                if not isinstance(symbol,str):
                    raise ValueError("Template format error.")
                if symbol not in vars:
                    raise ValueError(f"Found undefined symbol in template: {symbol}")
        
        for item in vars:
            # ensure that the type assignings in template["var_types"] are supported (Formula, SetVariable, ClassVariable)
            if template["var_types"][item] not in [Formula, SetVariable, ClassVariable]:
                raise ValueError(f"Found unsupported type in template: {item}:{template['var_types'][item]}")
        
    def __str__(self):
        temp_str = ""
        for symbol in self.template["template"]:
            if isinstance(symbol, str):
                temp_str += f" {symbol} "
            else:
                temp_str += f" {symbol.label} "
        vartype_str = ""
        for v in self.template["var_types"].keys():
            vartype_str += f"{v} : {self.template['var_types'][v].__name__}\n"
        return f"Template: {temp_str}\nTypes:\n{vartype_str}"





if __name__=='__main__':
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