# Units

[Rivtlib Index](../README.md#rivtlib-index) /
[Rivtlib](./index.md#rivtlib) /
Units

> Auto-generated documentation for [rivtlib.units](https://github.com/rivtlib/rivtlib-code/blob/main/rivtlib/units.py) module.

#### Attributes

- `path1` - rivtcalc path information - comment out for more general: `importlib.util.find_spec('rivtcalc')`

- `K` - print(dir())
  standard SI units ==== DO NOT MODIFY BETWEEN DOUBLE LINES  ===================
  temperature conversion is relative degree size, not offset ------------: `new_unit('K', 0, 'kelvin')`

- `G` - ============  DO NOT MODIFY ABOVE THIS LINE  =================================
  metric units ----------------------------------------------------------: `new_unit('G', 9.80665 * M / S ** 2, 'gravity acceleration')`

- `IN` - imperial--------------------------------------------------------------
  length: `new_unit('in', M / 39.370079, 'inch')`

- `LBM` - mass: `new_unit('lbm', KG / 2.2046226, 'pound-mass')`

- `LBF` - force: `new_unit('lbs', 4.4482216 * N, 'pound-force')`

- `FT_KIPS` - moment: `new_unit('ft-kips', FT * LBF * 1000.0, 'foot-kips')`

- `SF` - area: `new_unit('sf', FT ** 2, 'square feet')`

- `PSF` - pressure: `new_unit('psf', LBF / FT ** 2, 'pounds per square foot')`

- `PCI` - density: `new_unit('pci', LBF / IN ** 3, 'pounds per cubic inch')`

- `KLI` - line loads: `new_unit('kips/in', KIPS / IN, 'kips per inch')`

- `HR` - time: `new_unit('hr', 60 * 60 * S, 'hours')`

- `MPH` - velocity: `new_unit('mph', MILES / HR, 'miles per hour')`


- [Units](#units)
