SDyPy Template Project
-----------------------

A template to help you start a new project in the SDyPy ecosystem.


Using the template
------------------

To use this template, you have multiple options. The following two will cover most use cases:

1. You can use GitHub's templating functionality. A new repository will be created on GitHub for your project. Use this option if your project does not yet have an online repository.
   
   Click the "Use this template" button on the project template Github repository (see image below).

    .. image:: images/use_template.png

   Simply select and confirm a name for your new repository, and a copy of this template will be created for you. 

   You can now clone your new repository onto your local machine. If your new repository is located at ``https://github.com/<your_name>/<my_new_project>``, for example:

    .. code-block:: console

        $ git clone https://github.com/<your_name>/<my_new_project>

   A folder named ``<my_new_project>`` will be created on your machine. It is already setup with a connection to your new GitHub repository, and you can begin developing your package!

2. If you already have a repository for your project, located for example at ``https://github.com/<your_name>/<my_existing_project>``, 
   you can use our template by cloning in onto you local machine. This downloads the files into a local folder, with a connection with the online repository already set up.
   Do this by running :

    .. code-block:: console

        $ git clone https://github.com/sdypy/sdypy_template_project

   Our template files will be downloaded into the ``sdypy_template_project`` folder. 
   
   You can now either copy these files into you existing local project folder, or connect the cloned repository in the ``sdypy_template_project`` folder with your existing online repository :

    .. code-block:: console

        $ git remote rm origin
        $ git remote add origin https://github.com/ladisk/<my_existing_project>.git

You are now setup to begin working on your project.

To begin development, create a virtual environment and install the project in
editable mode using `uv <https://github.com/astral-sh/uv>`_:

.. code-block:: console

    $ uv venv
    $ uv pip install -e ".[dev]"

All dependencies are declared in ``pyproject.toml``: the runtime ones under
``[project] dependencies``, the development and documentation ones under
``[project.optional-dependencies]`` (``dev`` and ``docs``).

Now you can replace the core source code modules in ``sdypy_template_project/`` with your code.

Remember to replace the project name (``sdypy_template_project``) with your own project name in the following files:

- ``pyproject.toml`` — ``name`` (the distribution name, and the self-reference in the ``dev`` extra), ``description``, ``keywords``, ``[project.urls]``
- ``README.rst``
- ``CONTRIBUTING.rst``
- ``docs/source/conf.py`` — ``project``, ``author``, ``copyright``
- ``sync_version.py`` — the ``package_name`` variable at the top
- ``.readthedocs.yaml`` — nothing project-specific, but check the Python version
- ``.github/workflows/release-and-publish-to-pypi.yml`` — the branch name in the ``git push`` step (``master`` or ``main``) and the PyPI project name in the ``environment`` ``url``
- the ``sdypy_template_project/`` directory name itself

Consider adding unit-tests for your project by modifying the files found in ``tests/``. The provided test file structure is setup to work with `pytest <https://docs.pytest.org/en/latest/>`_.

To also use the sphinx documentation, modify files in ``docs/source``, or remove the ``docs/`` folder and quickstart a fresh documentation version using the ``sphinx-quickstart`` command (see `Sphinx - Getting started <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_ for more info).


File structure
--------------

The project code is structured as follows:

pyproject.toml
    the main project configuration file: package metadata, dependencies, and build system

sync_version.py
    helper script to keep the version consistent across ``pyproject.toml``, ``__init__.py``, and ``docs/source/conf.py``

README.rst
    the main project description / documentation file

CONTRIBUTING.rst
    a document containing information for potential contributors (developers) of the package

License
    the project license

.github/
    GitHub Actions workflow definitions for CI testing and automated PyPI releases,
    and the Dependabot configuration that keeps those actions up to date

.readthedocs.yaml
    the Read the Docs build configuration (required by Read the Docs)

.gitignore
    defines the files in the project directory to be excluded from version control

tests/
    contains project unit-tests

sdypy_template_project/
    contains the core project source code, separated into meaningful sub-modules

examples/
    scripts and notebooks with examples to showcase the project

docs/
    the documentation source and built files


(For a more complex and customizable project structure, see the `Cookiecutter project <https://github.com/audreyr/cookiecutter-pypackage>`_.)


Version management
------------------

Use ``sync_version.py`` to keep the version consistent across ``pyproject.toml``, ``__init__.py``, and ``docs/source/conf.py``.

Bump the patch/minor/major version:

.. code-block:: console

    $ python sync_version.py --bump patch
    $ python sync_version.py --bump minor
    $ python sync_version.py --bump major

Or set an explicit version:

.. code-block:: console

    $ python sync_version.py --set-version 1.2.3

The script updates all three files in one step, so you never have to edit them manually.


Building the documentation
--------------------------

By setting up `ReadTheDocs <https://readthedocs.org/>`_, your project documentation can automatically be built and puclished as a publicly available website.

To test your documentation locally, install the documentation dependencies
(``uv pip install -e ".[docs]"``, already included in ``[dev]``) and run the
following (starting from the main project directory) :

.. code-block:: console

    $ cd docs
    $ make clean
    $ make html

Your documentation files will be built inside the ``docs/build/html`` folder.


Continuous integration
----------------------

The included GitHub Actions workflows run automatically once you push your project to GitHub:

- **Testing** (``.github/workflows/python-package.yml``) — runs flake8 and pytest on every push and pull request, across Python 3.10 to 3.14.
- **Release** (``.github/workflows/release-and-publish-to-pypi.yml``) — triggered when you push a ``v*`` tag; syncs the version, builds the distribution, creates a GitHub Release, and publishes to PyPI.

Publishing uses `PyPI Trusted Publishing <https://docs.pypi.org/trusted-publishers/>`_,
so no API token is stored in the repository. Register your GitHub repository as a
trusted publisher on PyPI with these values:

- **Workflow name:** ``release-and-publish-to-pypi.yml``
- **Environment name:** ``pypi``

For a project that is not yet on PyPI, add a *pending publisher* under *Account
settings → Publishing* and use the ``name`` from ``pyproject.toml`` as the PyPI
project name. The first tagged release creates the project. For a project that
already exists, go to *Your projects → Manage → Publishing* instead.

PyPI trusts only this exact workflow file name. If you rename the file, update the
trusted publisher on PyPI, or publishing fails.

The release job runs in the ``pypi`` GitHub environment. GitHub creates it on the
first run. To require manual approval before each release, add a protection rule
under *Settings → Environments → pypi*.

If you cannot use Trusted Publishing, the workflow contains a commented-out
fallback that uses a ``PYPI_API_TOKEN`` repository secret instead.

``.github/dependabot.yml`` opens a monthly pull request when a newer version of a
used GitHub Action is available; without it the actions quietly fall behind (and
eventually run on an unsupported Node runtime).


Publishing the project
----------------------

**Automated (recommended)**

1. Bump and sync the version:

.. code-block:: console

    $ python sync_version.py --bump patch

2. Commit, tag, and push:

.. code-block:: console

    $ git add -u
    $ git commit -m "bump version to X.Y.Z"
    $ git tag vX.Y.Z
    $ git push && git push --tags

The release workflow will build the package and publish it to PyPI automatically.

**Manual (fallback)**

Build the distribution:

.. code-block:: console

    $ python -m build

Test the resulting ``.whl`` locally in a fresh environment:

.. code-block:: console

    $ uv venv test-env
    $ uv pip install --python test-env dist/<sdypy_template_project-X.Y.Z>.whl

Upload to TestPyPI first to verify, then to the main index:

.. code-block:: console

    $ python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    $ python -m twine upload dist/*

For more information on the publishing process, see the `Python packaging tutorial <https://packaging.python.org/tutorials/packaging-projects/>`_.

Once published, the package can be installed with:

.. code-block:: console

    $ pip install sdypy-template-project

The distribution name (``sdypy-template-project``, used with ``pip``) matches the
import name (``sdypy_template_project``, used in Python) -- keep the two in sync
when you rename the project.

After installing sdypy_template_project you can use it like any other Python module.

Here is a simple example with the current example code:

.. code-block:: python

    import sdypy_template_project as iep
    import numpy as np
    import matplotlib.pyplot as plt

    video = np.load('examples/speckle.npy', mmap_mode='r')
    results = iep.get_displacements(video, point=[5, 5], roi_size=[7, 7])

    plt.figure()
    plt.plot(results[0], label='x [px]')
    plt.plot(results[1], label='y [px]')
    plt.legend()
    plt.show()

You can also run this basic example by running the following command in the project base direcotry:

.. code-block:: console

    $ python -m examples.basic_example

The `Read the Docs page <http://sdypy_template_project.readthedocs.io>`_ provides the project documentation.
