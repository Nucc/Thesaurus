Thesaurus plugin for Sublime Text 3
===

The plugin helps you in Sublime to find words related to a selected word or phrase and replace it with the chosen one.

The plugin uses Altervista as the default data source for providing synonyms alone. 

It can be configured to fetch many more kinds of related words using Datamuse API (http://www.datamuse.com/api/).

The plugin can support word associations given below:

  For single words or phrases:

  1. meaning similar to
  2. spells like
  3. sounds like
  4. related to topics/themes

  For single words alone

  1. popular adjectives for a noun
  2. popular nouns for an adjective
  3. specific synonyms
  4. associated words
  5. antonyms
  6. categories (hypernyms)    
  7. specific items in a category (hyponyms)
  8. wholes of a part (holonyms)
  9. part of a whole (meronyms)
  10. popular next words for the given word
  11. popular previous words for the given word
  12. rhyming words (exact, approximate or homophones)
  13. words with same consonants

The plugin can display meanings, pronunciations and usage frequencies of suggested words.

How to install
---

To enable smart suggestions for alternatives to words that are not found in the thesaurus, PyEnchant must be installed in the external python environment. This can by done by running the command `pip install -U pyenchant` in a terminal / command window.

Using Package Control
---

  1. If you use Package Control (http://wbond.net/sublime_packages/package_control), just install the <code>Thesaurus</code> plugin.

  2. Configure the data source

    1. Altervista

      1. Go to the next page and create a key:
      http://thesaurus.altervista.org/mykey

      2. Change your User preferences (<code>[CMD|CTRL]+SHIFT+P</code>, search for User preferences) and add the previous key:

      "thesaurus_api_key": "keyFromAltervista"

    2. Datamuse

      Change your User preferences (<code>[CMD|CTRL]+SHIFT+P</code>, search for User preferences) and add the following line:

      "thesaurus_data_source": "datamuse"

Install from repository
-----

  1. Find your packages directory. If you don't know where it is, Sublime will help you. On Windows and Linux find the Browse Packages menu, on OSX follow the next menu structure:

    1. Sublime Text 3
    2. Preferences
    3. Browse Packages


  2. Go to this folder in console

    $ cd ~/Library/Application Support/Sublime Text 3/Packages # on OSX
  3. Install the package

    $ git clone https://github.com/Nucc/Thesaurus

  4. Configure the data source

    1. Altervista

      1. Create the key for Altervista at http://thesaurus.altervista.org/mykey

      2. Add the API key to the Thesaurus.sublime-settings file:

      {
        "api_key": "pasteTheApiKeyHere"
      }

    2. Datamuse

      Configure Datamuse in the Thesaurus.sublime-settings file:

      {
        "data_source": "datamuse"
      }

      "thesaurus_data_source": "datamuse"

Usage
---

Select the word and press <code>(CMD/CTRL)+T</code>, or use the <code>(CMD/CTRL)+SHIFT+P</code> combo and search for Thesaurus.

When using Datamuse, modifiers can be added to selected text to obtain different kinds of related words. Modifiers are specified using the format "/<modifier> <values>". Modifiers can be combined to create a complex query for words that satisfy multiple conditions (only AND logic supported as of now). Simple synonym search is performed if the selected text does not start with a modifier.

|  |Word Relationship|Modifier|Supported values|Comments|
|-:|:-----------------:--------:---------------|:-------|
| 1|meaning similar to|/means or /m|Any word or phrase||
| 2|spells like|/spell or /sp|Any word or phrase|Wildcards are supported|
| 3|sounds like|/sounds or /sou|Any word or phrase||
| 4|related to topics/themes|/topics|Words, comma separated|Upto 5 topics|
| 5|popular adjectives for a noun|/adj|Nouns||
| 6|popular nouns for an adjective|/noun|Adjectives||
| 7|specific synonyms|/syn|Any word|More specific than 'means similar to'|
| 8|associated (trigger) words|/trigger or /tr|Any word||
| 9|antonyms|/ant|Any word||
|10|categories (hypernyms)|/category or /cat|Any word|Example: '/cat sweet' -> taste, treat, course|
|11|specific items in a category (hyponyms)|/specific or /spec|Any word|Example: '/spec taste' -> gum, candy, pudding|
|12|wholes of a part (holonyms)|/whole|Any word|Example: '/whole leg' -> table, frame, chair|
|13|parts of a whole (meronyms)|/part|Any word|Example: '/part leg -> foot, cuff, shank'|
|14|popular next words for a given word|/next|Any word|Example: '/next wreak' -> havoc|
|15|popular previous words for a given word|/prev|Any word|Example: '/prev havoc' -> wreak|
|16|exact rhyme|/rhyme or /rhy|Any word||
|17|approximate rhyme|/aprhyme or /apr|Any word|Example: '/apr robust' -> corrupt|
|18|homophones|/homophone or /hp|Any word|Same pronunciation but different spellings|
|19|words with matching consonants|/cons|Any word|Example: '/cons simple -> sample|

Some modifiers can be used to display more information about suggested words. These modifiers use the format "/<modifier>"

|  |Information|Modifier|Comments|
|-:|:----------|:-------|--------|
| 1|Meanings|/dict|Upto three meanings|
| 2|IPA pronunciation|/pron||
| 3|Word frequency|/freq|Uses per million words|

Contribution
---

Fork it, fix it, send it. Create an issue here in Github if you have any trouble.

Please star the project if you like it! Thanks! :)
