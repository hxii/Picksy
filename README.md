# Picksy
Python picker module with a simple search.

## Usage
```python
from picksy import Picksy

options = {
  'thing': "This is the greatest thing!",
  'else': "This is different!",
  'blabla': "Only the best stuff"
}

message = "Select a thing!\n"

p = Picksy(options=options, message=message)

print(f"Your choice was {(p.get_choice())}")
```
_Output_:
```
>>> Your choice was blabla
```

## Notes
- Picksy will also accept a `list` type for the `options` argument, and will transform it into a dictionary automagically.
- Picksy currently *doesn't* support multiple choice.
