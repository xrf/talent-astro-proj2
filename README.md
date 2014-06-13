Project 2
=========

This is the second project for the [TALENT course][1]:
[nuclear theory for astrophysics (2014)][2].


Table of contents
-----------------

  - [Roles](#roles)
  - [Topic](#topic)
  - [Building and running](#building-and-running)
  - [Input format](#input-format)
  - [Scripts for analysis](#scripts-for-analysis)

Roles
-----

  - **Analysis:**     Fei Yuan
  - **Code:**         Amber Lauer
  - **Parameter:**    Tsunghan Yeh

Topic
-----

Modelling [X-ray burst][5] [nucleosynthesis][6] with the XNet reaction network
solver, following the model of [Fisker et al (2007)][3]: the premade model for
a [CNO][4] X-ray burst.

Building and running
--------------------

Firstly, be sure to run the following script to generate `Makefile` using
`Makefile.in` as input:

    ./configure

The makefile can do several things:

  - download and unpack ReduceReaclib and XNet if necessary

  - compile ReduceReaclib and XNet

  - run XNet and ReduceReaclib with the parameters in:
      - `th`: thermodynamic trajectory
      - `ab`: initial abundance
      - `control`: control file
      - `sunet`: nuclide list

Note: XNet is run inside a subdirectory under `runs`.

Commonly used targets in the makefile are:

  - `all`: compile both `reducereaclib` and `xnet`

  - `reducereaclib`: compile ReduceReaclib

  - `xnet`: compile XNet

  - `clean`: delete the entire `dist` directory

  - `run`: equivalent to `run-xnet`

  - `run-xnet`: run XNet

  - `run-reducereaclib`: run ReduceReaclib

When compiling, the code for XNet and ReduceReaclib are automatically
downloaded to the `dist` directory.

For example, to run XNet in `runs/my_run`:

    make RUN_DIR=my_run run

Input format
------------

Here are the input formats inferred from the Fortran code as well as the
sample input files.  The formats here are shown using an [EBNF][7]-like
notation.

The `...` indicates that Fortran will ignore all trailing garbage on that line
so feel free to put whatever in there.

### Control file (`control`)

    <control> ::=
        "## Problem Description"                                    "\n"
        <str:description1>                                          "\n"
        <str:description2>                                          "\n"
        <str:description3>                                          "\n"
        "## Job Controls"                                           "\n"
        <int:initial_zone>                                      ... "\n"
        <int:num_of_zones>                                      ... "\n"
        <int:include_weak_reactions>                            ... "\n"
        <int:include_screening>                                 ... "\n"
        <int:process_nuclear_data_at_runtime>                   ... "\n"
        "## Integration Controls"                                   "\n"
        <int:choice_of_integration_scheme>                      ... "\n"
        <int:max_num_of_timesteps_before_quit>                  ... "\n"
        <int:max_iterations_per_step>                           ... "\n"
        <int:convergence_condition>                             ... "\n"
        <float:max_abundance_change_per_timestep>               ... "\n"
        <float:smallest_abundance_used_in_timestep_calculation> ... "\n"
        <float:mass_conservation_limit>                         ... "\n"
        <float:convergence_criterion>                           ... "\n"
        <float:lower_abundance_limit>                           ... "\n"
        <float:max_factor_to_change_dt_in_a_time_step>          ... "\n"
        "## Output Controls"                                        "\n"
        <int:diagnostic_output_level>                           ... "\n"
        <int:per_timestep_output_level>                         ... "\n"
                                                                ... "\n"
        <str:ascii_output_filename_root>                            "\n"
                                                                ... "\n"
        <str:binary_output_filename_root>                           "\n"
                                                                ... "\n"
        <str:nuclide>{repeat 14 times}                              "\n"
        "## Input Controls"                                         "\n"
                                                                ... "\n"
        <str:data_dir>                                              "\n"
                                                                ... "\n"
        (<str:ab_filename> "\n"
         <str:th_filename> "\n){repeat as many times as num_of_zones}

### Initial abundance (`ab`)

    <ab>    ::= <str:description>            "\n"
                (<item> <item> <item> <item> "\n")*
    <item>  ::= <str:nuclide> <float:abundance>

### Thermodynamic trajectory (`th`)

    <th>    ::= <str:description>        "\n"
                <float:start_time>   ... "\n"
                <float:stop_time>    ... "\n"
                <float:dt_initial>   ... "\n"
                <row>*
    <row>   ::= <float:time> <float:temperature> <float:density> ... "\n"

### Nuclide list (`sunet`)

    <sunet> ::= (<str:nuclide> "\n")*

Note that `<str:nuclide>` must be right-aligned and occupy exactly 5
characters.

Scripts for analysis
--------------------

Note: most of the Python codes require [Numpy][8], and some will also require
[Matplotlib][9] for visualization.

### `tso_reader.py`

Python module that reads the binary output files ("tso" files) from XNet.

This is based on a script originally written by Kevin Siegl.

### `dump-tso`

Reads a tso file and writes the abundances (as well as time) in an ASCII
format.  Nuclides that don't participate at all are excluded (i.e. sum of
abundances less than a certain threshold).

Dependencies:
  - `tso_reader.py`
  - `elements.py`

### `plot-tso`

Reads a tso file and plots the abundances against time.

Dependencies:
  - `tso_reader.py`
  - `elements.py`

### `plot-chart`

Reads a tso file and plots the abundances on the nuclear chart as an animation.

Dependencies:
  - `chart-all`
  - `chart-stable`
  - `tso_reader.py`

Note: requires `ffmpeg` to be installed, though you can also change the
encoder used by Matplotlib by modifying the script.

This is based on a script originally written by Kaitlin J. Cook.  Nuclear data
was provided by Kaitlin J. Cook (`chart-stable`) and Alison Dreyfuss
(`chart-all`).

[1]: http://nucleartalent.org
[2]: https://groups.nscl.msu.edu/jina/talent/wiki/Course_7
[3]: http://dx.doi.org/10.1086/519517
[4]: http://en.wikipedia.org/wiki/CNO_cycle
[5]: http://en.wikipedia.org/wiki/X-ray_burster
[6]: http://en.wikipedia.org/wiki/Nucleosynthesis
[7]: http://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_Form
[8]: http://numpy.org
[9]: http://matplotlib.org
