# Str R

[Rivtlib Index](../README.md#rivtlib-index) /
[Rivtlib](./index.md#rivtlib) /
Str R

> Auto-generated documentation for [rivtlib.str_r](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py) module.

- [Str R](#str-r)
  - [R2rst](#r2rst)
    - [R2rst().attach](#r2rst()attach)
    - [R2rst().project](#r2rst()project)
    - [R2rst().r_rst](#r2rst()r_rst)
    - [R2rst().report](#r2rst()report)
    - [R2rst().search](#r2rst()search)
  - [R2utf](#r2utf)
    - [R2utf().attach](#r2utf()attach)
    - [R2utf().parseRutf](#r2utf()parserutf)
    - [R2utf().project](#r2utf()project)
    - [R2utf().report](#r2utf()report)
    - [R2utf().search](#r2utf()search)

## R2rst

[Show source in str_r.py:142](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L142)

convert rivt-strings to reST strings

#### Arguments

- `exportS` *str* - stores values that are written to file
- `strL` *list* - calc rivt-strings
- `folderD` *dict* - folder paths
- `tagD` *dict* - tag dictionary

#### Signature

```python
class R2rst:
    def __init__(self, strL: list, folderD: dict, tagD: dict):
        ...
```

### R2rst().attach

[Show source in str_r.py:345](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L345)

#### Signature

```python
def attach(self, rsL):
    ...
```

### R2rst().project

[Show source in str_r.py:257](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L257)

insert tables or text from csv, xlsx or txt file

#### Arguments

- `rL` *list* - parameter list

Files are read from /docs/docfolder
The command is identical to itable except file is read from docs/info.

#### Signature

```python
def project(self, rL):
    ...
```

### R2rst().r_rst

[Show source in str_r.py:234](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L234)

parse repository string

#### Returns

- `rstS` *list* - utf formatted calc-string (appended)
- `setsectD` *dict* - section settings

#### Signature

```python
def r_rst(self) -> str:
    ...
```

### R2rst().report

[Show source in str_r.py:348](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L348)

skip info command for utf calcs

Command is executed only for docs in order to
separate protected information for shareable calcs.

#### Arguments

- `rL` *list* - parameter list

#### Signature

```python
def report(self, rL):
    ...
```

### R2rst().search

[Show source in str_r.py:254](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L254)

#### Signature

```python
def search(self, rsL):
    ...
```



## R2utf

[Show source in str_r.py:34](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L34)

convert repo-string to UTF8 calc

#### Signature

```python
class R2utf:
    def __init__(self, strL: list, folderD: dict, tagD: dict):
        ...
```

### R2utf().attach

[Show source in str_r.py:94](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L94)

[summary]

#### Arguments

- `rsL` *[type]* - [description]

#### Signature

```python
def attach(self, rutfL):
    ...
```

### R2utf().parseRutf

[Show source in str_r.py:55](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L55)

parse rivt-string to UTF

#### Arguments

- `cmdL` *list* - command list
- `methL` *list* - method list
- `tagL` *list* - tag list

#### Signature

```python
def parseRutf(self, strL: list, cmdD: dict, cmdL: list, methL: list):
    ...
```

### R2utf().project

[Show source in str_r.py:91](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L91)

#### Signature

```python
def project(self, rutfL):
    ...
```

### R2utf().report

[Show source in str_r.py:102](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L102)

skip info command for utf calcs

Command is executed only for docs in order to
separate protected information for shareable calcs.

#### Arguments

- `rL` *list* - parameter list

#### Signature

```python
def report(self, rutfL):
    ...
```

### R2utf().search

[Show source in str_r.py:83](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/str_r.py#L83)

[summary]

#### Arguments

- `rsL` *[type]* - [description]

#### Signature

```python
def search(self, rutfL):
    ...
```


