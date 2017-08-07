Thesaurus plugin for Sublime
===

The plugin helps you in Sublime to find synonyms for the selected word and replace it with the chosen one.

How to install
---

To enable smart suggestions for alternatives to words that are not found in the thesaurus, PyEnchant must be installed in the external python environment. This can be done by running the command `pip install -U pyenchant` in a terminal / command window.

Using Package Control
---

  1. If you use Package Control (http://wbond.net/sublime_packages/package_control), just install the <code>Thesaurus</code> plugin.

  2. Go to the next page and create a key:

    http://thesaurus.altervista.org/mykey

  3. Change your User preferences (<code>[CMD|CTRL]+SHIFT+P</code>, search for User preferences) and add the previous key:

    "thesaurus_api_key": "keyFromAltervista"



Install from repository
-----

  1. Find your packages directory. If you don't know where it is, Sublime will help you. On Windows and Linux find the Browse Packages menu, on OSX follow the next menu structure:

    1. Sublime Text 2
    2. Preferences
    3. Browse Packages


  2. Go to this folder in console

    $ cd ~/Library/Application Support/Sublime Text 2/Packages    # on OSX

  3. Install the package

    $ git clone https://github.com/Nucc/Thesaurus

  4. Create an API key on Altervista.

    http://thesaurus.altervista.org/mykey

  5. Add the API key to the Thesaurus.sublime-settings file:

    {
      "api_key": "pasteTheApiKeyHere"
    }

Usage
---

Select the word and press <code>(CMD/CTRL)+T</code>, or use the <code>(CMD/CTRL)+SHIFT+P</code> combo and search for Thesaurus.

Contribution
---

Fork it, fix it, send it. Create an issue here in Github if you have any trouble.

Please star the project if you like it! Thanks! :)
