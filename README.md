# scb
An Python 3.* application to interact with the swedish statistical institute, Statistiska Centralbyrån (SCB).

# Exambples
>>> import scb
>>> s = scb.scb()
>>> s.print()
+---------------------------------+------+
|              Table              | Code |
+---------------------------------+------+
|   Ämnesövergripande statistik   |  AA  |
|          Arbetsmarknad          |  AM  |
|            Befolkning           |  BE  |
| Boende, byggande och bebyggelse |  BO  |
|              Energi             |  EN  |
|          Finansmarknad          |  FM  |
|  Handel med varor och tjänster  |  HA  |
|        Hushållens ekonomi       |  HE  |
|       Hälso- och sjukvård       |  HS  |
|    Jord- och skogsbruk, fiske   |  JO  |
|        Kultur och fritid        |  KU  |
|       Levnadsförhållanden       |  LE  |
|            Demokrati            |  ME  |
|              Miljö              |  MI  |
|       Nationalräkenskaper       |  NR  |
|        Näringsverksamhet        |  NV  |
|        Offentlig ekonomi        |  OE  |
|      Priser och konsumtion      |  PR  |
|           Socialtjänst          |  SO  |
| Transporter och kommunikationer |  TK  |
|     Utbildning och forskning    |  UF  |
+---------------------------------+------+
# Enter a specific table:
>>> s.enter('OE')
>>> s.enter('OE108')
>>> s.enter('OFFEkoMott')
# Request data from the table you're at:
>>> output = s.get() 
>>> output.keys()
dict_keys(['filters', 'values'])
# The dict output contains the filters the user specified and the values the database returned

