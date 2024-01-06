====================
Clean Business Chart
====================


.. image:: https://img.shields.io/pypi/v/clean_business_chart.svg
        :target: https://pypi.python.org/pypi/clean_business_chart

.. image:: https://readthedocs.org/projects/clean-business-chart/badge/?version=latest
        :target: https://clean-business-chart.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Clean Business Chart is a Python package for IBCS-like charts based on matplotlib. Currently a column chart with waterfall and a barchart with waterfall are supported


* Free software: MIT license
* Documentation: https://github.com/MarcelW1323/clean_business_chart/wiki.


Features
--------

* ColumnWithWaterfall, the first chart released with clean-business-chart (version 0.1.0)

  * added support for pandas in version 0.1.1

  * added date column support for pandas DataFrame and added translation of column headers inside the call in version 0.1.2

  * fixed error with FC-scenario when all FC-values were zero in version 0.2.12

* BarWithWaterfall, the second chart released in version 0.2.2

  * added support for parameter sort_chart in version 0.2.4

  * added support for parameter footnote in version 0.2.6

  * added support for parameter figsize in version 0.2.7 for optional (manual) sizing of the chart

  * better calculation of vertical part of figsize in version 0.2.8 for automatic sizing of the chart

  * added support for parameter translate_scenario in version 0.2.9 for optional translating the standard scenarios on the output of the chart
  
  * added support for parameter scalingvalue in version 0.2.10 for optional visualizing a scaling band. Also better visibility of texts. And added support for parameter figsize to only use x-size in float or integer

  * later rounding in the process leads to better connection between the waterfall and the total bars in version 0.2.11

* General

  * better rounding support for values of chart-labels in version 0.2.5


Read more
---------

* README.MD on github: https://github.com/MarcelW1323/clean_business_chart/blob/main/README.md
* LinkedIn Group on Clean Business Chart: https://www.linkedin.com/groups/12783685/


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
