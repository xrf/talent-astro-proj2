Project 2
=========

This is the second project for the [TALENT course][1]:
[nuclear theory for astrophysics (2014)][2].

[1]: http://nucleartalent.org
[2]: https://groups.nscl.msu.edu/jina/talent/wiki/Course_7

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

[3]: http://dx.doi.org/10.1086/519517
[4]: http://en.wikipedia.org/wiki/CNO_cycle
[5]: http://en.wikipedia.org/wiki/X-ray_burster
[6]: http://en.wikipedia.org/wiki/Nucleosynthesis

Building and running
--------------------

Firstly, be sure to run the following script to generate `Makefile` using
`Makefile.in` as input:

    ./configure

The makefile can do several things:

  - download and unpack ReduceReaclib and XNet if necessary

  - compile ReduceReaclib and XNet

  - run XNet and ReduceReaclib with the parameters in:
      - `th`
      - `ab`
      - `control`
      - `sunet`

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

    make run RUN_DIR=my_run
