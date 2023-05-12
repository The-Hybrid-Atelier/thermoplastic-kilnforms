# README

# The Kilnforms Ontology

The ontology is composed of three core concepts:

* Material
* Technique
* Form

# Malleable Form Calculator

A Malleable Form Calculator is a command-line interface that leverages the ontology to determine compatible thermoplastics in a kiln firing. 

## Installation Requirement
You need a python version 3 or higher executable to run the script.
To install required libraries, run:
```bash
pip install owlready2
pip install editdistance
```

## Determining the Malleable Form of a Thermoplastic

  * -h, --help            show this help message and exit
  * -m MATERIALS [MATERIALS ...], --materials MATERIALS [MATERIALS ...]
                        The materials to be fired.
  * -f FIRING, --firing FIRING
                        The firing temperature of the kiln (default: Celsius).
  * -T TEMPERATURE_UNIT, --temperature_unit TEMPERATURE_UNIT
                        C = Celsius, F= Fahrenheit, K=Kelvin
  * -q QUERY, --query QUERY
                        Query the Kilnforms Ontology

### Example Queries


How does ABS react when fired at 285ºC?
```python
python kilnforms.py -T C -m ABS -f 285
```

How does ABS react when fired at 285ºF?
```python
python kilnforms.py -F C -m ABS -f 285
```

How does a composite of ABS and PC react when fired at 285ºC?
``` python
python kilnforms.py -T C -m ABS PC -f 285
```

How does a composite of ABS, PC and PLA react when fired at 285ºC?
``` python
python kilnforms.py -T C -m ABS PC PLA -f 285
```

What thermoplastics can I use in kilnforming?
``` python 
python kilnforms.py -q Thermoplastic
```

What kilnforming techniques are possible?
``` python 
python kilnforms.py -q Technique
```



