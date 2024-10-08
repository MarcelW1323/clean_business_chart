=======
History
=======

0.2.19 (2024-10-01)
-------------------

* Fixed a small bug with forecast information in special cases when no usable visual was produced


0.2.18 (2024-09-15)
-------------------

* Added parameter 'highlight' in bar chart with waterfall to highlight detail bars.
* Added parameter 'last_closed_month' in column chart with waterfall to indicate last used month for actual values


0.2.17 (2024-07-07)
-------------------

* Improved support for parameter sort_chart also in combination with year or month fields in bar chart with waterfall


0.2.16 (2024-05-25)
-------------------

* Fixed disconnected lines bug in some cases by later rounding in the total values of the bar chart


0.2.15 (2024-03-04)
-------------------

* Added parameter 'footnote' and related 'footnote_size' in column chart with waterfall for supporting footnotes for example to mention the source.
* Centralized function for display of the footnote so bar chart with waterfall and column chart with waterfall share the same code base


0.2.14 (2024-01-26)
-------------------

* Fixed waterfall pattern-bug in bar chart with waterfall


0.2.13 (2024-01-26)
-------------------

* Fixed cosmetic bug with AC-scenario when total equals zero in column chart with waterfall


0.2.12 (2024-01-06)
-------------------

* Fixed error with FC-scenario when all FC-values were zero


0.2.11 (2023-12-23)
-------------------

* Later rounding in the process leads to better connection between the waterfall and the total bars


0.2.10 (2023-12-14)
-------------------

* Added parameter 'scalingvalue' in bar chart with waterfall for optional visualizing a scaling band. Improved chart with better visibility of texts. And added support for parameter 'figsize' for providing the x-size


0.2.9 (2023-11-26)
------------------

* Added parameter 'translate_scenario' in bar chart with waterfall for optional translating the standard scenarios on the output of the chart.


0.2.8 (2023-11-18)
------------------

* Better calculation of vertical part of figsize for automatic sizing of the bar chart with waterfall.


0.2.7 (2023-11-12)
------------------

* Added parameter 'figsize' in bar chart with waterfall for optional (manual) sizing of the chart.


0.2.6 (2023-10-29)
------------------

* Added parameter 'footnote' and related 'footnote_size' in bar chart with waterfall for supporting footnotes for example to mention the source.


0.2.5 (2023-10-15)
------------------

* Better rounding support for value labels in charts.


0.2.4 (2023-09-26)
------------------

* Added parameter 'sort_chart' in bar chart with waterfall for supporting ordinal categories-of-interest.


0.2.2 (2023-09-14)
------------------

* Second chart: bar chart with waterfall. Small bug occured on Google Colab, not at local installation. Other solution.


0.2.1 (2023-09-12)
------------------

* Second chart: bar chart with waterfall. Small bug occured on Google Colab, not at local installation. Bugfix wasn't succesfull.


0.2.0 (2023-09-12)
------------------

* Second chart: bar chart with waterfall.


0.1.2 (2023-04-11)
------------------

* Added date column in pandas DataFrame support in parameter data when calling the column chart with waterfall.
* Also added translate_headers as a parameter in dictionary-form to rename the columns within the call.


0.1.1 (2023-03-29)
------------------

* Added pandas DataFrame support in parameter data when calling the column chart with waterfall.


0.1.0 (2023-02-21)
------------------

* First release on PyPI. Column chart with waterfall.

