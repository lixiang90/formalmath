# Formal mathematics package on python

Formal mathematics package on python.

Support a proof check system core equivalent to [metamath](us.metamath.org)

 ## Install

```
pip install formalmath
```

## Example use

Here is an example for propositional logic.

```python
from formalmath.metamath import FormalSystem

# 1. Define constants in the system.
constants = ['wff', '->', '|-', '(', ')', '-.']

# 2. Define axioms.
axioms = {
    'wi': {
        'd': {},
        't': {
            'wph': 'wff ph',
            'wps': 'wff ps'
        },
        'h': {},
        'a': 'wff ( ph -> ps )'
    },
    'wn': {
        'd': {},
        't': {
            'wph': 'wff ph'
        },
        'h': {},
        'a': 'wff -. ph'
    },
    'ax-1': {
        'd': {},
        't': {
            'wph': 'wff ph',
            'wps': 'wff ps'
        },
        'h': {},
        'a': '|- ( ph -> ( ps -> ph ) )'
    },
    'ax-2': {
        'd': {},
        't': {
            'wph': 'wff ph',
            'wps': 'wff ps',
            'wch': 'wff ch'
        },
        'h': {},
        'a': '|- ( ( ph -> ( ps -> ch ) ) -> ( ( ph -> ps ) -> ( ph -> ch ) ) )'
    },
    'ax-3': {
        'd': {},
        't': {
            'wph': 'wff ph',
            'wps': 'wff ps'
        },
        'h': {},
        'a': '|- ( ( -. ph -> -. ps ) -> ( ps -> ph ) )'
    },
    'ax-mp': {
        'd': {},
        't': {
            'wph': 'wff ph',
            'wps': 'wff ps'
        },
        'h': {
            'min': '|- ph',
            'maj': '|- ( ph -> ps )'
        },
        'a': '|- ps'
    }
}

# 3. Instantiate FormalSystem.
fs = FormalSystem(constants=constants, axioms=axioms, theorems={})

# 4. Write a new theorem for the system.
mp2 = {
    'd': {},
    't': {
        'wph': 'wff ph',
        'wps': 'wff ps',
        'wch': 'wff ch'
    },
    'h': {
        'mp2.1': '|- ph',
        'mp2.2': '|- ps',
        'mp2.3': '|- ( ph -> ( ps -> ch ) )'
    },
    'a': '|- ch',
    'p':[
        'wps',
        'wch',
        'mp2.2',
        'wph',
        'wps',
        'wch',
        'wi',
        'mp2.1',
        'mp2.3',
        'ax-mp',
        'ax-mp'
    ]
}

# 5. Check the proof steps of the previous theorem in the formal system.
trace = fs._proof_check(mp2, detailed=True)
for tr in trace:
    print(tr)
```

The output will be

```cmd
Step 1: push type assumption 'wps' -> 'wff ps'
Step 2: push type assumption 'wch' -> 'wff ch'
Step 3: push hypothesis 'mp2.2' -> '|- ps'
Step 4: push type assumption 'wph' -> 'wff ph'
Step 5: push type assumption 'wps' -> 'wff ps'
Step 6: push type assumption 'wch' -> 'wff ch'
Step 7: apply axiom 'wi', pop ['wff ps', 'wff ch']
  match wph: type 'wff', var 'ph' -> 'ps'
  match wps: type 'wff', var 'ps' -> 'ch'
  conclude -> 'wff ( ps -> ch )' and push to stack
Step 8: push hypothesis 'mp2.1' -> '|- ph'
Step 9: push hypothesis 'mp2.3' -> '|- ( ph -> ( ps -> ch ) )'
Step 10: apply axiom 'ax-mp', pop ['wff ph', 'wff ( ps -> ch )', '|- ph', '|- ( ph -> ( ps -> ch ) )']
  match wph: type 'wff', var 'ph' -> 'ph'
  match wps: type 'wff', var 'ps' -> '( ps -> ch )'
  hypothesis min matches '|- ph'
  hypothesis maj matches '|- ( ph -> ( ps -> ch ) )'
  conclude -> '|- ( ps -> ch )' and push to stack
Step 11: apply axiom 'ax-mp', pop ['wff ps', 'wff ch', '|- ps', '|- ( ps -> ch )']
  match wph: type 'wff', var 'ph' -> 'ps'
  match wps: type 'wff', var 'ps' -> 'ch'
  hypothesis min matches '|- ps'
  hypothesis maj matches '|- ( ps -> ch )'
  conclude -> '|- ch' and push to stack
Proof successfully concludes with assertion '|- ch'
```

