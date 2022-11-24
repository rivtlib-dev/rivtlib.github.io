---
layout: default
title: Utils
parent: Unum
---


# Core

[Rivtlib Index](../../README.md#rivtlib-index) /
[Rivtlib](../index.md#rivtlib) /
[Unum](./index.md#unum) /
Core

> Auto-generated documentation for [rivtlib.unum.core](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py) module.

- [Core](#core)
  - [Formatter](#formatter)
    - [Formatter().configure](#formatter()configure)
    - [Formatter().format](#formatter()format)
    - [Formatter().format_number](#formatter()format_number)
    - [Formatter().format_unit](#formatter()format_unit)
  - [UnitTable](#unittable)
    - [UnitTable().get_definition](#unittable()get_definition)
    - [UnitTable().is_basic](#unittable()is_basic)
    - [UnitTable().is_derived](#unittable()is_derived)
    - [UnitTable().new_unit](#unittable()new_unit)
    - [UnitTable().reset](#unittable()reset)
  - [Unum](#unum)
    - [Unum().assert_no_unit](#unum()assert_no_unit)
    - [Unum().cast_unit](#unum()cast_unit)
    - [Unum().copy](#unum()copy)
    - [Unum().format_number](#unum()format_number)
    - [Unum().format_unit](#unum()format_unit)
    - [Unum().is_basic](#unum()is_basic)
    - [Unum().match_units](#unum()match_units)
    - [Unum().max_level](#unum()max_level)
    - [Unum().number](#unum()number)
    - [Unum().replaced](#unum()replaced)
    - [Unum.reset_format](#unumreset_format)
    - [Unum.set_format](#unumset_format)
    - [Unum().simplify_unit](#unum()simplify_unit)
    - [Unum.uniform](#unumuniform)
    - [Unum().unit](#unum()unit)
  - [uniform_unum](#uniform_unum)

## Formatter

[Show source in core.py:70](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L70)

#### Signature

```python
class Formatter(object):
    def __init__(self, **kwargs):
        ...
```

### Formatter().configure

[Show source in core.py:88](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L88)

#### Signature

```python
def configure(self, **kwargs):
    ...
```

### Formatter().format

[Show source in core.py:146](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L146)

Return our string representation, normalized if applicable.

Normalization occurs if Unum.AUTO_NORM is set.

#### Signature

```python
def format(self, value):
    ...
```

### Formatter().format_number

[Show source in core.py:140](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L140)

#### Signature

```python
def format_number(self, value):
    ...
```

### Formatter().format_unit

[Show source in core.py:100](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L100)

#### Signature

```python
def format_unit(self, value):
    ...
```



## UnitTable

[Show source in core.py:15](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L15)

#### Signature

```python
class UnitTable(dict):
    ...
```

### UnitTable().get_definition

[Show source in core.py:22](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L22)

#### Signature

```python
def get_definition(self, symbol):
    ...
```

### UnitTable().is_basic

[Show source in core.py:25](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L25)

#### Signature

```python
def is_basic(self, symbol):
    ...
```

### UnitTable().is_derived

[Show source in core.py:28](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L28)

#### Signature

```python
def is_derived(self, symbol):
    ...
```

### UnitTable().new_unit

[Show source in core.py:31](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L31)

#### Signature

```python
def new_unit(self, symbol, definition=BASIC_UNIT, name=""):
    ...
```

#### See also

- [BASIC_UNIT](#basic_unit)

### UnitTable().reset

[Show source in core.py:16](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L16)

#### Signature

```python
def reset(self, table=None):
    ...
```



## Unum

[Show source in core.py:176](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L176)

Encapsulates a value attached to a unit.

Implements arithmetic operators, dynamic unit consistency checking, and
string representation.

#### Signature

```python
class Unum(object):
    def __init__(self, value, unit=None, normal=False):
        ...
```

### Unum().assert_no_unit

[Show source in core.py:307](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L307)

#### Raises

- `ShouldBeUnitlessError` -  if self has a unit

#### Signature

```python
def assert_no_unit(self):
    ...
```

### Unum().cast_unit

[Show source in core.py:233](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L233)

Return a Unum with this Unum's value and the units of the given Unum.

Raises IncompatibleUnitsError if self can't be converted to other.
Raises NonBasicUnitError if other isn't a basic unit.

#### Signature

```python
@uniform_unum
def cast_unit(self, other):
    ...
```

#### See also

- [uniform_unum](#uniform_unum)

### Unum().copy

[Show source in core.py:221](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L221)

Return a copy of this Unum, normalizing the copy if specified.

#### Signature

```python
def copy(self, normalized=False):
    ...
```

### Unum().format_number

[Show source in core.py:392](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L392)

#### Signature

```python
def format_number(self, func):
    ...
```

### Unum().format_unit

[Show source in core.py:395](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L395)

#### Signature

```python
def format_unit(self, func):
    ...
```

### Unum().is_basic

[Show source in core.py:251](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L251)

#### Signature

```python
def is_basic(self):
    ...
```

### Unum().match_units

[Show source in core.py:348](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L348)

Return (self, other) where both Unums have the same units.

Raises IncompatibleUnitsError if there is no way to do this.
If there are multiple ways to do this, the units of self, then other
are preferred, and then by maximum level.

#### Signature

```python
def match_units(self, other):
    ...
```

### Unum().max_level

[Show source in core.py:316](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L316)

#### Returns

the maximum level of self's units

#### Signature

```python
def max_level(self):
    ...
```

### Unum().number

[Show source in core.py:323](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L323)

Return the (normalized) raw value of self.

If other is supplied, first convert to other's units before returning
the raw value.

Raises NonBasicUnitError if other is supplied, but has a value other
than 1. (e.g., kg.number(2*g) is an error, but kg.number(g) is ok.)

#### Signature

```python
def number(self, unit=None):
    ...
```

### Unum().replaced

[Show source in core.py:256](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L256)

Return a Unum with the string u replaced by the Unum conv_unum.

If u is absent from self, a copy of self is returned.

#### Signature

```python
def replaced(self, symbol, definition):
    ...
```

### Unum.reset_format

[Show source in core.py:204](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L204)

#### Signature

```python
@classmethod
def reset_format(cls):
    ...
```

### Unum.set_format

[Show source in core.py:200](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L200)

#### Signature

```python
@classmethod
def set_format(cls, **kwargs):
    ...
```

### Unum().simplify_unit

[Show source in core.py:269](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L269)

Normalize our units IN PLACE and return self.

Substitutions may be applied to reduce the number of different units,
while making the fewest substitutions.

If forDisplay is True, then prefer a single unit to no unit.

#### Signature

```python
def simplify_unit(self, forDisplay=False):
    ...
```

### Unum.uniform

[Show source in core.py:186](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L186)

Return a unitless Unum if value is a number.

If value is a Unum already, it is returned unmodified.

#### Signature

```python
@staticmethod
def uniform(value):
    ...
```

### Unum().unit

[Show source in core.py:218](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L218)

#### Signature

```python
def unit(self):
    ...
```



## uniform_unum

[Show source in core.py:169](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/core.py#L169)

#### Signature

```python
def uniform_unum(func):
    ...
```


