import sublime, sublime_plugin
import urllib
import json
import re
import sys
import os
alternativesLocation = os.path.join(os.path.abspath(os.path.dirname(__file__)), "alternatives.py")

class NoResultError(Exception):
  def __init__(self, message):
    self.message = message;

  def __str__(self):
    return repr(self.message)

class ThesaurusCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.result = []
    self.region = False
    self.value = ""
    self.edit = edit

    # process our selected word
    self.processWord(self.selected_word())

  def noAction(self, value):
    pass

  def processWord(self, word):
    self.word = word
    if self.word is None or len(self.word) == 0:
      sublime.active_window().show_quick_panel(["Please select a word first!"], self.noAction)
      return

    try:
      self.results = self.synonyms()
      sublime.active_window().show_quick_panel(self.results, self.valueIsSelected)
    except NoResultError:
      # nothing was found, look for alternatives
      self.alternatives = ["No results were found for '%s'!, try one of the following:" % self.word]
      self.alternatives.extend(self.get_alternative_words())
      sublime.active_window().show_quick_panel(self.alternatives, self.alternativeIsSelected)

  def alternativeIsSelected(self, value):
    if value > 1:
      self.processWord(self.alternatives[value])

  def valueIsSelected(self, value):
    if value != -1:
      self.replace(self.results[value])

  def selected_word(self):
    for region in self.view.sel():
      if not region.empty():
        self.region = region
        return self.view.substr(region)

  def replace(self, value):
    if not self.region or value is None or len(value) == 1:
      return

    value = re.subn(r'\(.*?\)$', "", value)[0]
    if value is not None:
      self.view.replace(self.edit, self.region, value.strip().lower())

  def synonyms(self):
    result = []
    data = self.get_json_from_api()
    try:
      for entry in data["response"]:
        result.append(entry["list"]["synonyms"].split("|"))
    except KeyError:
      raise NoResultError(data["error"])

    r = list(set([item for sublist in result for item in sublist]))
    r.sort()
    return r

  def get_json_from_api(self):
    f = urllib.urlopen("http://thesaurus.altervista.org/thesaurus/v1?key=%s&word=%s&language=en_US&output=json" % (self.api_key(), urllib.quote(self.word)))
    content = f.read()
    f.close()
    return json.loads(content)

  def api_key(self):
    settings = sublime.load_settings('Thesaurus.sublime-settings')
    if settings.get("api_key"):
      return settings.get("api_key")
    else:
      settings = sublime.load_settings('Preferences.sublime-settings')
      return settings.get("thesaurus_api_key")

  def get_alternative_words(self):
    # dirty hack around not being able to use enchant in sublime
    import subprocess
    p = subprocess.Popen(["python", alternativesLocation, self.word], stdout=subprocess.PIPE)
    alternativesString = p.communicate()[0]
    p.stdout.close()
    alternatives = []
    # this will replace the alternatives var
    exec alternativesString
    if alternatives[0] == "error":
      print "Enchant error: %s, defaulting to dummy method..." % alternatives[1] 
      # nope, an error occurred, do it the dummy way
      suffixes = ["es", "s", "ed", "er", "ly", "ing"]
      alternatives = []
      for suffix in suffixes:
        if self.word.endswith(suffix):
          alternatives.append(self.word[:(-1*len(suffix))]);
    return alternatives