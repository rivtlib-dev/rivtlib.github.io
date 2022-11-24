---
layout: default
title: Utils
parent: Unum
---



# Utils

[Rivtlib Index](../../README.md#rivtlib-index) /
[Rivtlib](../index.md#rivtlib) /
[Unum](./index.md#unum) /
Utils

> Auto-generated documentation for [rivtlib.unum.utils](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/utils.py) module.

- [Utils](#utils)
  - [as_number](#as_number)
  - [as_unit](#as_unit)
  - [as_unum](#as_unum)
  - [decode](#decode)
  - [encode](#encode)
  - [is_unit](#is_unit)
  - [uarray](#uarray)
  - [unitless](#unitless)

## as_number

[Show source in utils.py:50](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/utils.py#L50)

Using:
as_number(value, [places=])
as_number(value, to_unit, [places=])
as_number(value, from_unit, to_unit, [places=])

#### Arguments

- `value` - float or unum value to conversion
- `from_unit` - unit which value has when is given as float or int
- `to_unit` - unit for which numeric value is getting
- `places` - round argument

#### Returns

evaluated float value

#### Signature

```python
def as_number(value, *args, **kwargs):
    ...
```



## as_unit

[Show source in utils.py:46](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/utils.py#L46)

#### Signature

```python
def as_unit(value):
    ...
```



## as_unum

[Show source in utils.py:33](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/utils.py#L33)

#### Signature

```python
def as_unum(value, unit=None):
    ...
```



## decode

[Show source in utils.py:89](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/utils.py#L89)

#### Signature

```python
def decode(number):
    ...
```



## encode

[Show source in utils.py:81](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/utils.py#L81)

#### Signature

```python
def encode(number):
    ...
```



## is_unit

[Show source in utils.py:29](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/utils.py#L29)

#### Signature

```python
def is_unit(value):
    ...
```



## uarray

[Show source in utils.py:5](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/utils.py#L5)

Convenience function to return a Unum containing a numpy array.
With current versions of numpy, we have the following undesirable behavior:

```python
>>> from unum.units import M
>>> array([5,6,7,8]) * M
array([5 [m], 6 [m], 7 [m], 8 [m]], dtype=object)
```

#### Arguments

- `array_like` - numpy array
- `args` - args given to numpy array
- `kwargs` - kwargs given to numpy

#### Returns

Unum containing numpy array

#### Signature

```python
def uarray(array_like, *args, **kwargs):
    ...
```



## unitless

[Show source in utils.py:23](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/utils.py#L23)

#### Signature

```python
def unitless(*values):
    ...
```


