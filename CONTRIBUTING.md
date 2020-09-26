# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions
### Report Bugs

Report bugs at https://github.com/jvfe/reconciler/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

reconciler could always use more documentation, whether as part of the official reconciler docs, in docstrings, or even on the web in blog posts, articles, and such. To write documentation, check out the docs/ directory, and become familiar with [mkdocs](https://www.mkdocs.org/) - it's very easy.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/jvfe/reconciler/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Get Started!

Ready to contribute? Here's how to set up reconciler for local development.

* Fork the reconciler repo on GitHub.

* Clone your fork locally:

```bash
$ git clone git@github.com:your_name_here/reconciler.git
```

* Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:

```bash
$ mkvirtualenv reconciler
$ cd reconciler/
$ python setup.py develop
```

* Create a branch for local development:

```bash
$ git checkout -b name-of-your-bugfix-or-feature
```

Now you can make your changes locally.

* When you're done making changes, check that your changes are black-formatted and pass the tests:

```bash
$ black reconciler tests
$ python setup.py test or pytest
$ pytest
```

To get black, just pip install it into your virtualenv.

* Add your name to the docs/authors.md file.

* Commit your changes and push your branch to GitHub:

```bash
$ git add .
$ git commit -m "Your detailed description of your changes."
$ git push origin name-of-your-bugfix-or-feature
```

* Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, if your pull request includes code changes check that it meets these guidelines:

* The pull request should include tests.
* If the pull request adds functionality, the docs should be updated. 
    * Put your new functionality into a function with a docstring, and update the docs/reference files.
* Make sure your code changes were formatted with the Black styling tool.

## Tips

To run a subset of tests:

```bash
$ pytest tests.test_reconciler
```