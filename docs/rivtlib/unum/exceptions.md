---
layout: default
title: Exceptions
parent: Unum
---




# Exceptions

[Rivtlib Index](../../README.md#rivtlib-index) /
[Rivtlib](../index.md#rivtlib) /
[Unum](./index.md#unum) /
Exceptions

> Auto-generated documentation for [rivtlib.unum.exceptions](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/exceptions.py) module.

- [Exceptions](#exceptions)
  - [ConversionError](#conversionerror)
  - [IncompatibleUnitsError](#incompatibleunitserror)
  - [NameConflictError](#nameconflicterror)
  - [NonBasicUnitError](#nonbasicuniterror)
  - [ShouldBeUnitlessError](#shouldbeunitlesserror)
  - [UnumError](#unumerror)

## ConversionError

[Show source in exceptions.py:29](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/exceptions.py#L29)

Failed to convert a unit to the desired type.

#### Signature

```python
class ConversionError(UnumError):
    def __init__(self, u):
        ...
```

#### See also

- [UnumError](#unumerror)



## IncompatibleUnitsError

[Show source in exceptions.py:18](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/exceptions.py#L18)

An operation on two Unums failed because the units were incompatible.

#### Signature

```python
class IncompatibleUnitsError(TypeError):
    def __init__(self, unit1, unit2):
        ...
```



## NameConflictError

[Show source in exceptions.py:38](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/exceptions.py#L38)

Tried to define a symbol that was already defined.

#### Signature

```python
class NameConflictError(UnumError):
    def __init__(self, unit_key):
        ...
```

#### See also

- [UnumError](#unumerror)



## NonBasicUnitError

[Show source in exceptions.py:47](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/exceptions.py#L47)

Expected a basic unit but got a non-basic unit.

#### Signature

```python
class NonBasicUnitError(UnumError):
    def __init__(self, u):
        ...
```

#### See also

- [UnumError](#unumerror)



## ShouldBeUnitlessError

[Show source in exceptions.py:9](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/exceptions.py#L9)

An operation on a Unum failed because it had units unexpectedly.

#### Signature

```python
class ShouldBeUnitlessError(TypeError):
    def __init__(self, u):
        ...
```



## UnumError

[Show source in exceptions.py:1](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/unum/exceptions.py#L1)

A Unum error occurred that was unrelated to dimensional errors.

#### Signature

```python
class UnumError(Exception):
    ...
```


