"""
Post Statistics
========================

This plugin calculates various statistics about a post and stores them in an article.stats dictionary:

wc: how many words
read_mins: how many minutes to read this article, based on 250 wpm (http://en.wikipedia.org/wiki/Words_per_minute#Reading_and_comprehension)
word_counts: frquency count of all the words in the article; can be used for tag/word clouds/
fi: Flesch-kincaid Index/ Reading Ease
fk: Flesch-kincaid Grade Level

"""

import re
from collections import Counter

from pelican import signals
from pelican.contents import Article, Page
from pelican.generators import ArticlesGenerator, PagesGenerator
from bs4 import BeautifulSoup

from .readability import text_stats, flesch_index, flesch_kincaid_level


def calculate_stats(instance):
    """
    Calculate the statistics for a given instance.
    """

    if type(instance) in (Article, Page) and instance._content is not None:
        stats = {}
        content = instance._content

        # How fast do average people read?
        WPM = 250

        # Use BeautifulSoup to get readable/visible text
        raw_text = BeautifulSoup(content, 'html.parser').getText()

        # Process the text to remove entities
        entities = r'\&\#?.+?;'
        raw_text = raw_text.replace('&nbsp;', ' ')
        raw_text = re.sub(entities, '', raw_text)

        # Flesch-kincaid readbility stats counts sentances,
        # so save before removing punctuation
        tmp = raw_text

        # Process the text to remove punctuation
        drop = '.,?!@#$%^&*()_+-=\\|/[]{}`~:;\'\"‘’—…“”'
        raw_text = raw_text.translate({ord(c): '' for c in drop})

        # Count the words in the text
        words = raw_text.lower().split()
        word_count = Counter(words)

        # Return the stats
        stats['word_counts'] = word_count
        stats['wc'] = sum(word_count.values())

        # Calulate how long it'll take to read, rounding up
        stats['read_mins'] = (stats['wc'] + WPM - 1) // WPM
        if stats['read_mins'] == 0:
            stats['read_mins'] = 1

        # Calculate Flesch-kincaid readbility stats
        readability_stats = stcs, words, sbls = text_stats(tmp, stats['wc'])
        stats['fi'] = f"{flesch_index(readability_stats):.2f}"
        stats['fk'] = f"{flesch_kincaid_level(readability_stats):.2f}"

        instance.statistics = stats
        # For backward compatibility added the same in `stats` as well
        instance.stats = stats


def run_plugin(generators):
    """Run the Statistics plugin."""
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                calculate_stats(article)
                for translation in article.translations:
                    calculate_stats(translation)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                calculate_stats(page)
                for translation in page.translations:
                    calculate_stats(translation)


def register():
    """Register the Statistics plugin."""
    try:
        signals.all_generators_finalized.connect(run_plugin)
    except AttributeError:
        # NOTE: This results in #314 so shouldn't really be relied on
        # https://github.com/getpelican/pelican-plugins/issues/314
        signals.content_object_init.connect(calculate_stats)
