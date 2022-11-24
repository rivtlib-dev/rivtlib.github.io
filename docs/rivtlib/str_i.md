# Str I

[Rivtlib Index](../README.md#rivtlib-index) /
[Rivtlib](./index.md#rivtlib) /
Str I

> Auto-generated documentation for [rivtlib.str_i](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_i.py) module.

- [Str I](#str-i)
  - [I2rst](#i2rst)
    - [I2rst().i_rst](#i2rst()i_rst)
  - [I2utf](#i2utf)
    - [I2utf().e_utf](#i2utf()e_utf)

## I2rst

[Show source in str_i.py:396](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_i.py#L396)

convert rivt-strings to reST strings

#### Arguments

- `exportS` *str* - stores values that are written to file
- `strL` *list* - calc rivt-strings
- `folderD` *dict* - folder paths
- `setcmdD` *dict* - command settings
- `setsectD` *dict* - section settings
- `rivtD` *dict* - global rivt dictionary

#### Signature

```python
class I2rst:
    def __init__(
        self,
        strL: list,
        folderD: dict,
        setcmdD: dict,
        setsectD: dict,
        rivtD: dict,
        exportS: str,
    ):
        ...
```

### I2rst().i_rst

[Show source in str_i.py:500](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_i.py#L500)

parse insert-string

#### Returns

- `calcS` *list* - utf formatted calc-string (appended)
- `setsectD` *dict* - section settings
- `setcmdD` *dict* - command settings

#### Signature

```python
def i_rst(self) -> tuple:
    ...
```



## I2utf

[Show source in str_i.py:41](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_i.py#L41)

convert insert-string to UTF8 calc

#### Signature

```python
class I2utf:
    def __init__(self, strL: list, folderD, cmdD, sectD):
        ...
```

### I2utf().e_utf

[Show source in str_i.py:148](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_i.py#L148)

parse eval-string

#### Returns

- `calcS` *list* - utf formatted calc-string (appended)
- `setsectD` *dict* - section settings
- `setcmdD` *dict* - command settings

#### Signature

```python
def e_utf(self) -> tuple:
    ...
```


