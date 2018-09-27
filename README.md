# scb
An Python 3.* application to interact with the swedish statistical institute, Statistiska Centralbyrån (SCB).

# Example
> import scb
> s = scb.scb()
Print content at current level:
`s.print()`
Enter a specific table:
`s.enter('OE')
`s.enter('OE108')
s.enter('OFFEkoMott')
Request data from the table you're at:
`output = s.get()`
Output will be a dict with entries "filters" and "values", respectively containing the filters the user specified and the values the database returned.
