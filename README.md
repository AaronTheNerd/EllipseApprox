
# Ellipse Perimeter Estimate Generator

> This program brute force generates formulas which approximate the perimeter of an ellipse.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running](#running)
- [Specifications](#specifications)
  - [Obtaining Actual Values](#obtaining-actual-values)
  - [Calculator](#calculator)
  - [Registering Approximations](#registering-approximations)
  - [Testing](#testing)
  - [Plotting](#plotting)
  - [Multiprocessing](#multiprocessing)
- [Examples](#examples)

## Installation
> Please ensure that you have both Python 3.10 and pipenv installed on your machine

```shell
$ pipenv install
```

> This should begin the installation of all required dependencies. If you would like to skip this step, the provided Pipfile can be used to install the dependencies manually.

## Configuration

> The preferred method of customizing the output of this code is to modify the `configs.json` file. Below is an example `configs.json`.

```json
{
    "subprocess_count": 6,
    "approx": {
        "max_stack_size": 20,
        "max_test_score": 400000,
        "save_current_best": true,
        "calc_prefix": ["math.pi", "EllipseProperties.a", "EllipseProperties.b", "ops.ADD_OP", "ops.MUL_OP"],
        "constants": {
            "min_value": 1,
            "max_value": 11,
            "step": 1,
            "include_pi": true,
            "include_ellipse_properties": true
        },
        "filters": {
            "primitive_subformulas": false
        }
    },
    "plot": {
        "data": {
            "dimensions": 1,
            "min_value": 1,
            "max_value": 21, 
            "step": 0.05,
            "precision": 50
        },
        "style_sheet": "plot.mplstyle",
        "image_filename": "images/plot.png",
        "title": "Approximation Comparison",
        "xlabel": "Ellipse Ratio (a/b)",
        "ylabel": "Error (%)"
    },
    "test": {
        "data": {
            "dimensions": 2,
            "min_value": 0.5,
            "max_value": 20.5, 
            "step": 0.5,
            "precision": 10
        }
    },
    "interface": {
        "cli": {
            "enabled": true,
            "events": {
                "PROGRAM_STARTED": true,
                "APPROX_TESTED": true,
                "APPROX_SUBMITTED": true,
                "PROGRAM_FINISHED": true
            }
        },
        "fileio": {
            "enabled": true,
            "events": {
                "PROGRAM_STARTED": true,
                "APPROX_SUBMITTED": true
            }
        },
        "email": {
            "enabled": true,
            "events": {
                "APPROX_SUBMITTED": true
            },
            "kwargs": {
                "dev_email": "",
                "dev_password": "",
                "recipient_email": "",
                "benchmarks": ["Simple", "MattParker1", "Ramanujan1", "Ramanujan2"]
            }
        }
    }
}
```

> Below is an explanation of the configuration ptions

- `subprocess_count`(int): Specifies the number of subprocesses which should be used to generate the ellipse perimeter approximations. See [Multiprocessing](#multiprocessing) for more info.
- `approx`: An object which contains all ellipse perimeter approximation specifications.
  - `max_stack_size`(int): The maximum number of elements an ellipse perimeter approximation can contain.
  - `max_test_score`(float): Specifies the highest test score which can be recorded. See [Testing](#testing) for more info.
  - `save_current_best`(boolean): Determines whether or not the `max_test_score` number should be updated to the test score of the lowest test score which has been generated.
  - `calc_prefix`(list[string]): Specifies what each ellipse perimeter approximation should begin with. Valid elements include:
    - Any string which can be converted into an int or float
    - "ops.ADD_OP"
    - "ops.SUB_OP"
    - "ops.MUL_OP"
    - "ops.DIV_OP"
    - "ops.EXP_OP"
    - "ops.NEG_OP"
    - "ops.SQRT_OP"
    - "ops.INV_OP"
    - "EllipseProperties.a"
    - "EllipseProperties.b"
    - "EllipseProperties.c"
    - "EllipseProperties.e"
    - "EllipseProperties.h"
  - `constants`: An object specifing what constants should be included in the generated approximations
    - `min_value`(float): Inclusive, the minimum value of a constant.
    - `max_value`(float): Exclusive, the maximum value of a constant.
    - `step`(float): The amount between consecutive constants.
    - `include_pi`(boolean): Whether or not $\pi$ should be added to approximations
    - `include_ellipse_properties`(boolean): Whether or not the various ellipse properties (a, b, c, e, and h) should be included in approximations.
  - `filters`: (WIP) An object which determines which filters should be active.
    - `primitive_subformulas`(boolean): Determines whether or not subformulas which result in another constant value should be included in generated approximations.
- `plot`: (WIP) An object which contains all configuration plotting information. See [Plotting](#plotting) for more information.
  - `data`: An object specifying the configuration of the data used to plot approximations.
    - `dimensions`(int): Should be left at 1.
    - `min_value`(float): The minimum value of the x-axis which should be plotted.
    - `max_value`(float): The maximum value of the x-axis which should be plotted.
    - `step`(float): The difference between consecutive points.
    - `precision`(int): The number of terms which should be used to calculate the actual value of the ellipses. See [Obtaining Actual Values](#obtaining-actual-values) for more information.
  - `style_sheet`(string): A file location for an external matplotlib style sheet. See [here](https://matplotlib.org/1.5.3/users/style_sheets.html) for more information.
  - `image_filename`(string): The file location where the plot should be saved.
  - `title`(string): The title which should appear above the plot.
  - `xlabel`(string): The label for the x-axis.
  - `ylabel`(string): The label for the y-axis.
- `test`:
  - `data`:
    - `dimensions`(int):
    - `min_value`(float):
    - `max_value`(float): 
    - `step`(float):
    - `precision`(int):
- `interface`:
  - `cli`:
    - `enabled`(boolean):
    - `events`:
      - `PROGRAM_STARTED`(boolean):
      - `APPROX_TESTED`(boolean):
      - `APPROX_SUBMITTED`(boolean):
      - `PROGRAM_FINISHED`(boolean):
  - `fileio`:
    - `enabled`(boolean):
    - `events`:
      - `PROGRAM_STARTED`(boolean):
      - `APPROX_SUBMITTED`(boolean):
  - `email`:
    - `enabled`(boolean):
    - `events`:
      - `APPROX_SUBMITTED`(boolean):
    - `kwargs`:
      - `dev_email`(string):
      - `dev_password`(string):
      - `recipient_email`(string):
      - `benchmarks`(list[str]):

## Running

> The provided Makefile comes with a handful of rules to make running different parts this program simpler.

Running the main program
```shell
$ make run
```
---
To run the main program manually
```shell
$ pipenv run python perimeter_approximation/main.py
```
---
Alternatively, you could activate the pipenv before running
```shell
$ pipenv source
$ python perimeter_approximation/main.py
```
If you use the last method, make sure you deactivate the pipenv after running with
```shell
$ deactivate
```

## Specifications

> Below are some technical specifications for this program.

### Obtaining Actual Values

> Being able to calculate the actual perimeter of an ellipse is necessary for properly testing the performance of the generated ellipse perimeter approximations.

The following infinite sum is how this program calculates the actual perimeter of an ellipse

$$
    \pi(a+b)\left[1+\sum^{\infty}_{n=1}\left(\frac{(2n - 1)!!}{2^n n!}\right)^2\frac{h^n}{(2n-1)^2}\right]
$$

When the "precision" property is set in `configs.json`, it determines how many terms in the above summation are used.

### Calculator

> The Calculator object is incredibly important as it allows the program to model something as complicated as a mathematical formula as a simple data structure.

The Calculator object is an implementation of a stack based calculator. A stack based calculator is simply a list of constants and functions that finds a result by performing the following algorithm:

1. Iterate through the list.
2. If the current element is a constant, add it to the number stack.
3. If the current element is some sort of function or operator, remove the required amount of numbers from the number stack, apply said function to those numbers and add its result back into the stack.

#### Example:

The following calculator can find the distance to some point (x, y)

`Calculator([2, x, ^, 2, y, ^, +, sqrt])`

This is because the calculator will be resolved in the following way

1. elem = 2, num_stack = $\left[2\right]$
2. elem = x, num_stack = $\left[2, x\right]$
3. elem = ^, num_stack = $\left[x^2\right]$
4. elem = 2, num_stack = $\left[x^2, 2\right]$
5. elem = y, num_stack = $\left[x^2, 2, y\right]$
6. elem = ^, num_stack = $\left[x^2, y^2\right]$
7. elem = +, num_stack = $\left[y^2+x^2\right]$
8. elem = $\sqrt{}$, num_stack = $\left[\sqrt{y^2+x^2}\right]$

Therefore $\sqrt{y^2+x^2}$ is equivalent to `Calculator([2, x, ^, 2, y, ^, +, sqrt])`

**Note:** When using an operator/function which takes >1 input values, the function is supplied the values in the reverse order as how they were put in the original calculator i.e. in order to get the value 1/2, the calculator should be [2, 1, /] as opposed to [1, 2, /]

### Registering Approximations

> Registering approximations is a simple way to access previously found approximations anywhere in the program. 

Registering approximations requires modifications to the source code for this project. It is recommended that these modifications be placed in the file `perimeter_approximations/approximates.py`.

### Testing

> WIP

### Plotting

> WIP

### Multiprocessing

> WIP

## Examples



| Plot | Test Score | Simplified Formula | Calculator |
| ---- | ---------- | ------------------ | ---------- |
| ![plot1](/AaronTheNerd/EllipseApprox/blob/main/images/plot1.png?raw=true) | 1731 | $\pi\left(a+b\right)\left(3-\sqrt{4-h}\right)$ | `Calculator([3.141592653589793, EllipseProperties.a, EllipseProperties.b,ops.ADD_OP, ops.MUL_OP, ops.INV_OP, 6, EllipseProperties.h, ops.ADD_OP, 10, ops.SUB_OP, ops.SQRT_OP, 3, ops.SUB_OP, ops.DIV_OP])` |
| ![plot7](/AaronTheNerd/EllipseApprox/blob/main/images/plot7.png?raw=true) | 1319 | $\pi\left(a+b\right)\left(\frac{184329-1792\sqrt{h}}{143367}\right)^h$ | `Calculator([math.pi, EllipseProperties.a, EllipseProperties.b, ops.ADD_OP, ops.MUL_OP, ops.INV_OP, EllipseProperties.h, 8, 4, ops.EXP_OP, ops.SQRT_OP, ops.INV_OP, 8, 10, ops.MUL_OP, ops.ADD_OP, EllipseProperties.h, ops.SQRT_OP, ops.DIV_OP, 7, 9, ops.DIV_OP, ops.SUB_OP, ops.EXP_OP, ops.DIV_OP])` |
| ![plot2](/AaronTheNerd/EllipseApprox/blob/main/images/plot2.png?raw=true) | 909 | $\pi\left(a+b\right)\left(\frac{117}{5}-3h\right)^{7h\frac{\pi}{6^\pi}}$ | `Calculator([math.pi, EllipseProperties.a, EllipseProperties.b, ops.ADD_OP, ops.MUL_OP, math.pi, 6, ops.EXP_OP, math.pi, ops.DIV_OP, EllipseProperties.h, 7, 3, EllipseProperties.h, 5, 6, ops.DIV_OP, 9, ops.SUB_OP, ops.SUB_OP, ops.MUL_OP, ops.EXP_OP, ops.EXP_OP, ops.EXP_OP, ops.MUL_OP])` |
| ![plot3](/AaronTheNerd/EllipseApprox/blob/main/images/plot3.png?raw=true) | 814 | $\pi\left(a+b\right)\left(1+\sqrt{\frac{10-h}{24}}\right)^{h/2}$ | `Calculator([math.pi, EllipseProperties.a, EllipseProperties.b, ops.ADD_OP, ops.MUL_OP, 2, EllipseProperties.h, ops.DIV_OP, 1, 3, ops.INV_OP, 8, 9, EllipseProperties.h, 2, 2, ops.DIV_OP, ops.SUB_OP, ops.ADD_OP, ops.DIV_OP, ops.MUL_OP, ops.SQRT_OP, ops.ADD_OP, ops.EXP_OP, ops.MUL_OP])` |
| ![plot5](/AaronTheNerd/EllipseApprox/blob/main/images/plot5.png?raw=true) | 779 | $\pi(a+b)\left(\frac{1}{7}h+1\right)3^{h\sqrt{3}/18}$ | `Calculator([math.pi, EllipseProperties.a, EllipseProperties.b, ops.ADD_OP, ops.MUL_OP, 7, EllipseProperties.h, ops.ADD_OP, 7, 9, 8, 4, ops.SQRT_OP, 8, ops.SUB_OP, ops.DIV_OP, ops.SQRT_OP, EllipseProperties.h, ops.MUL_OP, ops.DIV_OP, 3, ops.EXP_OP, ops.DIV_OP, ops.MUL_OP, ops.MUL_OP])` |
| ![plot4](/AaronTheNerd/EllipseApprox/blob/main/images/plot4.png?raw=true) | 778 | $\pi\left(a+b\right)\left(\frac{\left(\frac{1}{h + 6}\right)^6}{8}+\frac{4}{3}\right)^{h/2}$ | `Calculator([math.pi, EllipseProperties.a, EllipseProperties.b, ops.ADD_OP, ops.MUL_OP, 2, EllipseProperties.h, ops.DIV_OP, 1, 3, ops.INV_OP, 8, 6, 1, 6, EllipseProperties.h, ops.ADD_OP, ops.INV_OP, ops.ADD_OP, ops.EXP_OP, ops.DIV_OP, ops.ADD_OP, ops.ADD_OP, ops.EXP_OP, ops.MUL_OP])` |
| ![plot6](/AaronTheNerd/EllipseApprox/blob/main/images/plot6.png?raw=true) | 767 | $\pi\left(a+b\right)\left(\frac{\pi}{\sqrt{6}}-\frac{h}{80-4^{-4}}\right)^h$ | `Calculator([math.pi, EllipseProperties.a, EllipseProperties.b, ops.ADD_OP, ops.MUL_OP, ops.INV_OP, EllipseProperties.h, 8, 4, ops.EXP_OP, ops.SQRT_OP, ops.INV_OP, 8, 10, ops.MUL_OP, ops.SUB_OP, EllipseProperties.h, ops.DIV_OP, 6, ops.SQRT_OP, math.pi, ops.DIV_OP, ops.SUB_OP, ops.EXP_OP, ops.DIV_OP])` |
