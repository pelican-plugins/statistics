Statistics: A Plugin for Pelican
====================================================

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/statistics/main.yml?branch=main)](https://github.com/pelican-plugins/statistics/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-statistics)](https://pypi.org/project/pelican-statistics/)
[![Downloads](https://img.shields.io/pypi/dm/pelican-statistics)](https://pypi.org/project/pelican-statistics/)
![License](https://img.shields.io/pypi/l/pelican-statistics?color=blue)

Pelican plugin that calculates post statistics such as word count, reading ease, and more.

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-statistics

As long as you have not explicitly added a `PLUGINS` setting to your Pelican settings file, then the newly-installed plugin should be automatically detected and enabled. Otherwise, you must add `statistics` to your existing `PLUGINS` list. For more information, please see the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

Usage
-----

This plugin to calculate various statistics about a post and store them in an `article.statistics` dictionary:

- `wc`: how many words
- `read_mins`: how many minutes would it take to read this article, based on 250 wpm (http://en.wikipedia.org/wiki/Words_per_minute#Reading_and_comprehension)
- `word_counts`: frquency count of all the words in the article; can be used for tag/word clouds
- `fi`: Flesch-kincaid Index/ Reading Ease (see: http://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)
- `fk`: Flesch-kincaid Grade Level

Example:

```python
{
    'wc': 2760,
    'fi': '65.94',
    'fk': '7.65',
    'word_counts': Counter({u'to': 98, u'a': 90, u'the': 83, u'of': 50, ...}),
    'read_mins': 12
}
```

This allows you to output these values in your templates, like this, for example:

```html
<p title="~{{ article.statistics['wc'] }} words">~{{ article.statistics['read_mins'] }} min read</p>
<ul>
    <li>Flesch-kincaid Index/ Reading Ease: {{ article.statistics['fi'] }}</li>
    <li>Flesch-kincaid Grade Level: {{ article.statistics['fk'] }}</li>
</ul>
```

The `word_counts` variable is a python `Counter` dictionary and looks something like this, with each unique word and it's frequency:

```python
Counter({u'to': 98, u'a': 90, u'the': 83, u'of': 50, u'karma': 50, .....
```

and can be used to create a tag/word cloud for a post.

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/statistics/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the AGPL-3.0 license.
