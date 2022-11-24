# Scan

[Rivtlib Index](../README.md#rivtlib-index) /
[Rivtlib](./index.md#rivtlib) /
Scan

> Auto-generated documentation for [rivtlib.scan](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/scan.py) module.

- [Scan](#scan)
  - [CheckDesign](#checkdesign)
    - [CheckDesign().varsummary](#checkdesign()varsummary)
  - [Checkrivt](#checkrivt)
    - [Checkrivt().filesummary](#checkrivt()filesummary)
    - [Checkrivt().logclose](#checkrivt()logclose)
    - [Checkrivt().logstart](#checkrivt()logstart)
    - [Checkrivt().logwrite](#checkrivt()logwrite)

## CheckDesign

[Show source in scan.py:69](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/scan.py#L69)

[summary]

#### Signature

```python
class CheckDesign:
    ...
```

### CheckDesign().varsummary

[Show source in scan.py:74](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/scan.py#L74)

variable summary table

#### Signature

```python
def varsummary():
    ...
```



## Checkrivt

[Show source in scan.py:10](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/scan.py#L10)

check rivt syntax and log

#### Arguments

- `logname` *[type]* - [description]

#### Returns

- `[type]` - [description]

#### Signature

```python
class Checkrivt:
    def __init__(self, logname):
        ...
```

### Checkrivt().filesummary

[Show source in scan.py:56](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/scan.py#L56)

file name summary table

#### Signature

```python
def filesummary():
    ...
```

### Checkrivt().logclose

[Show source in scan.py:45](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/scan.py#L45)

close log file

#### Signature

```python
def logclose(self):
    ...
```

### Checkrivt().logstart

[Show source in scan.py:24](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/scan.py#L24)

delete log file and initialize new file

#### Signature

```python
def logstart(self):
    ...
```

### Checkrivt().logwrite

[Show source in scan.py:34](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/scan.py#L34)

write processes to log file, option echo to terminal

#### Signature

```python
def logwrite(self, logstrg, flg=0):
    ...
```


