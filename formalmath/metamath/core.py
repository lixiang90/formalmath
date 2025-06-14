from typing import Dict, Optional, List, Union

class FormalSystem:
    def __init__(self, 
                 constants: Optional[List[str]],
                 axioms: Optional[Dict], 
                 theorems: Optional[Dict]={}, 
                 initial_data: Optional[Dict]=None
                 ):
        """
        A formal mathematics system class based on metamath
        See metamath book (https://us.metamath.org/downloads/metamath.pdf) Appendix C for detailed setting
        """
        if initial_data is not None:
            self.constants = initial_data['constants']
            self.axioms = initial_data['axioms']
            self.theorems = initial_data['theorems']
        else:
            assert constants is not None and axioms is not None and theorems is not None
            self.constants = constants
            self.axioms = axioms
            self.theorems = theorems
        
        # check label uniqueness and build namespace
        self.namespace = {}
        for c in self.constants:
            if c in self.namespace.keys():
                raise ValueError(f'{c}: duplicate constants')
            self.namespace[c] = 'constant'
        for a in self.axioms:
            if a in self.namespace.keys():
                raise ValueError(f'{a}: duplicate labels for axiom')
            self.namespace[a] = 'axiom'
            self.axioms[a] = self._check_(self.axioms[a])
        for p in self.theorems:
            if p in self.namespace.keys():
                raise ValueError(f'{p}: duplicate labels for theorem')    
            self.namespace[p] = 'theorem'
            self.theorems[p] = self._check_(self.theorems[p])
            assert self._proof_check(self.theorems[p]) is True, f"Proof of theorem {p} is wrong."
    
    def add_constant(self, constant: str):
        if constant in self.namespace:
            raise ValueError(f"Duplicate constant name: {constant}")
        self.constants.append(constant)
        self.namespace[constant] = 'constant'

    def add_axiom(self, label: str, axiom: Dict):
        if label in self.namespace:
            raise ValueError(f"Duplicate axiom name: {label}")
        self.axioms[label] = self._check_(axiom)

    def add_theorem(self, label: str, theorem: Dict):
        if label in self.namespace:
            raise ValueError(f"Duplicate axiom name: {label}")
        thm = self._check_(theorem)
        if not self._proof_check(thm):
            raise ValueError(f"Proof is incorrect: {label}")
        self.theorems[label] = thm
        


    def _check_(self, prop: Dict) -> Dict:
        """
        Check a proposition (statement) is well defined (not doing proof check here):
        1. prop is a dict with 4 keys 'd', 't', 'h', 'a' (axiom) or 5 keys 'd', 't', 'h', 'a', 'p' (theorem)
        2. key 't' has dict value, 
           each value is a string that has two segments splitted by space,
           first segment is a constant, second is not in namespace, called variable,
           each key and variable distinct and not in namespace.keys(), 
           example: 't': {'wph':'wff ph','wps':'wff ps'}
        3. key 'h' has dict value, 
           each value is a string that has several segments splitted by space,
           every segment is either a constant or a variable (from step 2),
           each key distinct, not in t's keys, not in variables, and not in namespace.keys()
           example: 'h': {'min':'|- ph','maj':'|- ( ph -> ps )'} 
        4. key 'a' has string value that has several segments splitted by space,
           every segment is either a constant or a variable (from step 2),
        5. key 'd' has dict value, 
           each value is a string that has two segments splitted by space,
           two segments are different variables (from step 2),
           each key distinct, not in t's keys, not in h's keys, not in variables, and not in namespace.keys()
        6. every variable got from step 2 appears at least once in values of 'h' and 'a'
        """
        # step 1: check prop keys
        allowed_keys_4 = {'d', 't', 'h', 'a'}
        allowed_keys_5 = {'d', 't', 'h', 'a', 'p'}
        prop_keys = set(prop.keys())
        assert prop_keys == allowed_keys_4 or prop_keys == allowed_keys_5, f'Wrong keys: {prop_keys}'
        # step 2: check 't' part and get all variables
        assert isinstance(prop['t'], dict), f'Wrong type assumption value: {prop['t']}'
        new_names = []
        variables = []
        for k in prop['t'].keys():
            assert k not in self.namespace.keys(), f'local name duplicate from global name: {k}'
            assert k not in new_names, f'local name duplicate from other local name: {k}'
            new_names.append(k)
            v = prop['t'][k]
            assert isinstance(v, str), f'Wrong value: {k}: {v}'
            v_split = v.split()
            assert len(v_split) == 2, f'Wrong value: {k}: {v}'
            assert v_split[0] in self.constants, f'prefix not constant: {k}: {v}'
            assert v_split[1] not in self.namespace and v_split[1] not in new_names and v_split[1] not in variables, f'variable name duplicate: {v_split[1]}'
            new_names.append(v_split[1])
            variables.append(v_split[1])

        # step 3: check 'h' hypotheses
        assert isinstance(prop['h'], dict), f'Wrong type hypotheses value: {prop["h"]}'
        hyp_names = []
        for k, v in prop['h'].items():
            assert k not in self.namespace and k not in new_names and k not in hyp_names, f'hypothesis label invalid or duplicate: {k}'
            hyp_names.append(k)
            assert isinstance(v, str), f'Hypothesis {k} must be a string'
            for token in v.split():
                assert token in self.constants or token in variables, f'Hypothesis {k} token invalid: {token}'

        # step 4: check 'a' assertion
        assert isinstance(prop['a'], str), f'Assertion must be a string: {prop["a"]}'
        for token in prop['a'].split():
            assert token in self.constants or token in variables, f'Assertion token invalid: {token}'

        # step 5: check 'd' distinct variable pairs
        assert isinstance(prop['d'], dict), f'Wrong type distinct value: {prop["d"]}'
        dist_names = []
        for k, v in prop['d'].items():
            assert k not in self.namespace and k not in new_names and k not in hyp_names and k not in dist_names, f'distinct label invalid or duplicate: {k}'
            dist_names.append(k)
            assert isinstance(v, str), f'Distinct {k} must be a string'
            v_split = v.split()
            assert len(v_split) == 2, f'Distinct {k} must have exactly two variables: {v}'
            var1, var2 = v_split
            assert var1 in variables and var2 in variables and var1 != var2, f'Distinct {k} variables invalid or same: {v}'

        # step 6: ensure each variable appears in at least one hypothesis or assertion
        used = set()
        for h in prop['h'].values():
            used.update([tok for tok in h.split() if tok in variables])
        for tok in prop['a'].split():
            if tok in variables:
                used.add(tok)
        missing = set(variables) - used
        assert not missing, f'Variables never used in hypotheses/assertion: {missing}'

        # if theorem, also check proof pointer 'p'
        if 'p' in prop:
            assert isinstance(prop['p'], (str,list)), f'Proof pointer must be a string: {prop["p"]}'

        # return normalized proposition
        return {
            'd': prop['d'],
            't': prop['t'],
            'h': prop['h'],
            'a': prop['a'],
            **({'p': prop['p']} if 'p' in prop else {})
        }
    
    def _proof_check(self, thm: Dict, detailed: bool=False) -> Union[bool, List[str]]:
        """
        check proof steps.
        Use RPN, maintain a stack for proof steps.
        1. when a proof step is a hypothesis ('t' or 'h' part), then push it into the proof stack
        2. when a proof step 'example' is an axiom, or a theorem proved before, then pop exactly same elements
        as the self.axioms['example']['t'].keys() + self.axioms['example']['h'].keys(), 
        apply the axiom or theorem to the poped elements exactly, then push the 'a' part we got.
        3. the apply procedue in step 2 is:
        3.1. compare 't' part to get a substitution table, ensure the typecode (first segment) match
        3.2. ensure that the distinct pairs in 'd' part has disjoint (in the sense of variables in substitution expressions) substitutions
        3.2. substitute variables to the corresponding expressions in h part and a part
        3.3. ensure every assumption in 'h' part is already in the 'h' part of the theorem to prove, or middle results proved in earlier steps.
        3.4. then, the 'a' part will be the output
        4. if after all steps, the result will be exactly the same as 'a' part in the theorem, then, the proof is verified. 
        """
        trace: List[str] = []
        stack: List[str] = []
        steps = thm['p'].split() if isinstance(thm['p'], str) else thm['p']
        for idx, step in enumerate(steps, 1):
            if step in thm['t']:
                expr = thm['t'][step]
                stack.append(expr)
                trace.append(f"Step {idx}: push type assumption '{step}' -> '{expr}'")
                continue
            if step in thm['h']:
                expr = thm['h'][step]
                stack.append(expr)
                trace.append(f"Step {idx}: push hypothesis '{step}' -> '{expr}'")
                continue
            # apply rule
            if step in self.axioms:
                rule = self.axioms[step]
                kind = 'axiom'
            elif step in self.theorems:
                rule = self.theorems[step]
                kind = 'theorem'
            else:
                raise AssertionError(f"Unknown proof step '{step}' at position {idx}")
            t_keys = list(rule['t'].keys())
            h_keys = list(rule['h'].keys())
            req_lbls = t_keys + h_keys
            n = len(req_lbls)
            if len(stack) < n:
                raise AssertionError(f"Stack underflow applying {step} at position {idx}")
            # pop and reorder
            popped = [stack.pop() for _ in range(n)]
            args = popped[::-1]
            trace.append(f"Step {idx}: apply {kind} '{step}', pop {args}")
            # substitution
            subs: Dict[str, str] = {}
            for lbl, expr in zip(t_keys, args[:len(t_keys)]):
                pat_type, var = rule['t'][lbl].split()
                tokens = expr.split()
                if tokens[0] != pat_type:
                    raise AssertionError(f"Type mismatch for {lbl}: expected '{pat_type}', got '{tokens[0]}' at step {idx}")
                subs[var] = ' '.join(tokens[1:])
                trace.append(f"  match {lbl}: type '{pat_type}', var '{var}' -> '{subs[var]}'")
            # distinct check
            for d_lbl, pair in rule['d'].items():
                v1, v2 = pair.split()
                if v1 in subs and v2 in subs:
                    if set(subs[v1].split()) & set(subs[v2].split()):
                        raise AssertionError(f"Distinct violation {d_lbl} at step {idx}")
            # hypothesis match
            for i, h_lbl in enumerate(h_keys, start=len(t_keys)):
                h_pat = rule['h'][h_lbl]
                expected = ' '.join(subs.get(tok, tok) for tok in h_pat.split())
                actual = args[i]
                if actual != expected:
                    raise AssertionError(f"Hypothesis mismatch for {h_lbl}: expected '{expected}', got '{actual}' at step {idx}")
                trace.append(f"  hypothesis {h_lbl} matches '{actual}'")
            # conclusion
            a_pat = rule['a']
            inst_a = ' '.join(subs.get(tok, tok) for tok in a_pat.split())
            stack.append(inst_a)
            trace.append(f"  conclude -> '{inst_a}' and push to stack")
        # final
        if len(stack) != 1 or stack[0] != thm['a']:
            raise AssertionError("Proof did not conclude with the theorem assertion")
        trace.append("Proof successfully concludes with assertion '{0}'".format(stack[0]))
        return trace if detailed else True

