# Str V

[Rivtlib Index](../README.md#rivtlib-index) /
[Rivtlib](./index.md#rivtlib) /
Str V

> Auto-generated documentation for [rivtlib.str_v](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_v.py) module.

- [Str V](#str-v)
  - [V2rst](#v2rst)
    - [V2rst().v_rst](#v2rst()v_rst)
  - [V2utf](#v2utf)

## V2rst

[Show source in str_v.py:319](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_v.py#L319)

#### Signature

```python
class V2rst:
    ...
```

### V2rst().v_rst

[Show source in str_v.py:320](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_v.py#L320)

parse value-string and set method

#### Returns

- `calcS` *list* - utf formatted calc-string (appended)
- `setsectD` *dict* - section settings
- `setcmdD` *dict* - command settings
- `rivtD` *list* - calculation results
- `exportS` *list* - value strings for export

#### Signature

```python
def v_rst(self) -> tuple:
    ...
```



## V2utf

[Show source in str_v.py:33](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_v.py#L33)

convert value-string to UTF8 calc

#### Signature

```python
class V2utf:
    def __init__(self, strL: list, folderD, cmdD, sectD):
        ...
```


