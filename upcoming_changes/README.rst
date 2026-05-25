This directory contains news fragments that are collected into ``CHANGELOG.rst``.

Each file should be named ``<ISSUE-OR-PR>.<TYPE>.rst`` where ``<TYPE>`` is one of:

* ``new``: a new user-facing feature.
* ``enhancements``: a user-visible improvement to existing functionality.
* ``bugfix``: a fix for incorrect behavior.
* ``api``: a public API addition or behavior change developers should track.
* ``deprecation``: a deprecated workflow, option, or API surface.
* ``doc``: a documentation improvement.
* ``maintenance``: tests, packaging, CI, contributor workflow, or other internal maintenance.

Keep fragments short and user-focused where possible.

To preview the generated changelog locally, run:

.. code-block:: bash

   towncrier build --draft
