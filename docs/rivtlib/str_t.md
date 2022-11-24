# Str T

[Rivtlib Index](../README.md#rivtlib-index) /
[Rivtlib](./index.md#rivtlib) /
Str T

> Auto-generated documentation for [rivtlib.str_t](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_t.py) module.

- [Str T](#str-t)
  - [T2utf](#t2utf)
    - [T2utf().t_rst](#t2utf()t_rst)

## T2utf

[Show source in str_t.py:5](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_t.py#L5)

convert insert-string to UTF8 calc

#### Signature

```python
class T2utf:
    def __init__(self, strL: list, folderD, cmdD, sectD):
        ...
```

### T2utf().t_rst

[Show source in str_t.py:24](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_t.py#L24)

parse table-strings

#### Returns

- `calcS` *list* - utf formatted calc-string (appended)
- `setsectD` *dict* - section settings
- `setcmdD` *dict* - command settings
- `rivtD` *list* - calculation values

#### Signature

```python
def t_rst(self) -> tuple:
    ...
```


