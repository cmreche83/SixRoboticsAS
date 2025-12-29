# Home Assignment: Python and Software Engineering

Welcome to the home assignment for Python and Software Engineering roles at Six Robotics.

Note: Please do not share this task or your solution with anyone outside of Six Robotics.

This task is intentionally open-ended and under-specified. Do your best to solve it as intended by the author. Please
document any assumptions you make and note any shortcomings in your solution.

Limit the scope of your work to approximately one evening, focusing on demonstrating your skills and versatility mainly
as a well rounded software engineer. Stubs and empty implementations can be used to speed up your work. However, ensure
that your solution runs as delivered.

It is not so important exactly what you implement, what we want to see is how you think think and deliver as an
engineer, and that we have a good foundation for technical discussions, code review and extensions during the technical
interview.

## Task

Your task is to make a _complete delivery_ on a project that aims to release a Python module publicly on GitHub under
the MIT license.

The module should implement a queuing system that is configured through a YAML file and returns a valid ordering of
jobs, either on CLI or as a return value from a function call.

It is allowed to use 3rd party dependencies.

Example of YAML input file:

```yaml
job_a:
job_b:
  dependencies:
    - foo
job_c:
  dependencies:
    - job_b
    - job_d
job_c_2:
job_d:
foo:
job_e:
  dependencies:
    - job_b
    - foo
    - job_a
```

Please send your solution to us as a ZIP file within 08:00 the day of the interview.

For the technical interview you will need to bring a laptop with development environment, so you can present, run and
modify you assignment.

Good luck! :)

## Implementation

This is a classic Graph Theory exercise where we are trying to design and optimise an oriented graph in order to minimise the amount of steps.
Mutiple scenarios can occur : 
- One solution : that's the ideal case
- No solution : in case of missing dependencies or multual dependencies

All yaml files have been located in the yaml subdirectory

- Python 3.12 was used for development.
- Code can be executed with Python 3+ (print() functions will not work on Python2 unless using __future__)
- requirements.txt have been provided (it should be possible to execute all of it with much older version of the packages provided in requirements.txt)
Use of venv directly or indirectly ( with uv ) is encouraged, alternatively I can provide a docker-compose file on demand.

This task has been implemented in main.py
This can be used as a package ( so can be imported and used as part of a larger program )
Unit tests are provided in tests.py (using unittest) and will use all of the yaml files provided
Messages in the commandline are available in color (Red for errors/exceptions)

Purposefully left debug code to let the reviewer understand more easily how the code works
It shows the name of the method without indentation in yellow 
before showing the checkpoint information (with indentation - relative to the method name ).
Debug information can be enabled by setting the debug to True in the constructor of the class 
( aka commented line in __main__ )

Code is (over)commented and docstring provided for each function to keep the purpose of everything clear

Further improvements for this task could be : 
- instead of relying on pyyaml for parsin yaml files, writting my own parser ( and provide more validity checks of the yaml file ).
- instead of only returning an object and/or printing it : exporting/representing the object in a CSV file (or SVG or XLS or ...)
- adding support for more fields than dependencies ( this being said, it would not be anymore a one evening job )
- providing more detailed and illustrated documentation ( for the task description in itself and the code provided )

Just to confirm : this has been written entirely without the use or help of an LLM/AI. Python Black has been used but nothing else.

Best regards,
Chris