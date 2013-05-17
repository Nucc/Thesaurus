import sublime, sublime_plugin
import urllib

class ThesaurusCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.result = []
    self.region = False
    self.value = ""
    self.edit = edit

    word = self.selected_word()
    if not word:
      return

    sublime.status_message = "Fetching synonyms from Thesaurus..."
    f = urllib.urlopen("http://words.bighugelabs.com/api/2/%s/%s/" % (self.api_key(), word))
    sublime.status_message = "Completed"

    for line in f.readlines():
      self.result.append(line.split("|")[-1].strip().lower())

    sublime.active_window().show_quick_panel(self.result, self.valueIsSelected)

  def valueIsSelected(self, value):
    if value != -1:
      self.replace(self.result[value])

  def selected_word(self):
    for region in self.view.sel():
      if not region.empty():
        self.region = region
        return self.view.substr(region)

  def replace(self, value):
    if not self.region or value is None or len(value) == 1:
      return

    self.view.replace(self.edit, self.region, value)

  def api_key(self):
    settings = sublime.load_settings('Thesaurus.sublime-settings')
    return settings.get("api_key")