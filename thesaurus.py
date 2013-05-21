import sublime, sublime_plugin
import urllib
import json
import re

class ThesaurusCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.result = []
    self.region = False
    self.value = ""
    self.edit = edit

    self.word = self.selected_word()
    if self.word is None or len(self.word) == 0:
      return

    self.results = self.synonyms()
    sublime.active_window().show_quick_panel(self.results, self.valueIsSelected)

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
    for entry in data["response"]:
      result.append(entry["list"]["synonyms"].split("|"))

    r = list(set([item for sublist in result for item in sublist]))
    r.sort()
    return r

  def get_json_from_api(self):
    f = urllib.urlopen("http://thesaurus.altervista.org/thesaurus/v1?key=%s&word=%s&language=en_US&output=json" % (self.api_key(), self.word))
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
