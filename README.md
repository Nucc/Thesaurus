Thesaurus plugin for Sublime
===

The plugin helps you in Sublime to find synonyms for the selected word and replace it with the chosen one.

How to install
---

  Find your packages directory. If you don't know where it is, Sublime will help you. On OSX follow the next menu structure:

    1. Sublime Text 2
    2. Preferences
    3. Browse Packages

  On Windows and Linux find the Browse Packages menu.

  Go to this folder in your console

    $ cd ~/Library/Application Support/Sublime Text 2/Packages    # on OSX

  Install the package

    $ git clone https://github.com/Nucc/Thesaurus

  Create an API key on Big Huge Labs.

    http://thesaurus.altervista.org/mykey

  Add the API key to the Thesaurus.sublime-settings file:

    {
      "api_key": "pasteTheApiKeyHere"
    }

  Select the word and press <code>(CMD/CTRL)+T</code>, or use the <code>(CMD/CTRL)+SHIFT+P</code> combo and search for Thesaurus.

Contribution
---

Fork it, fix it, send it. Create an issue here in Github if you have any trouble.