import sublime, sublime_plugin
import json
import re
import sys
import os
import copy

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.parse import quote
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import quote
    from urllib2 import urlopen
    from urllib2 import HTTPError

alternativesLocation = os.path.join(os.path.abspath(os.path.dirname(__file__)), "alternatives.py")

class NoResultError(Exception):
  def __init__(self, message):
    self.message = message;

  def __str__(self):
    return repr(self.message)

class LookupStrategy(object):
  @classmethod
  def synonyms(cls, word, language):
    """abstract"""

  @classmethod
  def get_json_from_api(cls, url):
    response = urlopen(url)
    content = response.read().decode('utf-8')
    response.close()
    return json.loads(content)

  @classmethod
  def synonyms(cls, word, language):
    return cls.synonyms_impl(word, language, cls.get_url, cls.extract_data)

  @classmethod
  def synonyms_impl(cls, word, language, get_url, extract_data):
    result = []
    try:
        data = cls.get_json_from_api(get_url(word, language))
        result = extract_data(data)
        if len(result) < 1:
          raise NoResultError("notfound")
    except (KeyError, HTTPError):
        if 'data' not in locals():
          raise NoResultError("error")
        else:
          raise NoResultError("notfound")
    return result

class AlterVistaLookup(LookupStrategy):
  @classmethod
  def extract_data(cls, data):
    result = []
    for entry in data["response"]:
        result.append(entry["list"]["synonyms"].split("|"))
    return list(set([item for sublist in result for item in sublist]))
    result.sort()

  @classmethod
  def get_url(cls, word, language):
      word = quote(word)
      return "http://thesaurus.altervista.org/thesaurus/v1?key=%s&word=%s&language=%s&output=json" % (cls.api_key(), word, language)

  @classmethod
  def api_key(cls):
    settings = sublime.load_settings('Thesaurus.sublime-settings')
    if settings.get("api_key"):
      return settings.get("api_key")
    else:
      settings = sublime.load_settings('Preferences.sublime-settings')
      return settings.get("thesaurus_api_key")

class DataMuseCommandSwitches(object):
  '''
  'means' is the default if there is no switch
  When switches are combined, words matching all specified switches
  are returned

  Switches:
    For single words or groups of words:
      /means (m)
      /spell (sp) - with wildcards * and ?
      /sounds (sou) - sounds like
      /topics - related to topics/themes (comma-separated, upto five)
      /dict - show dictionary meanings with words
      /pron - show pronunciation in IPA
      /freq - times seen per million

    For single words alone
      /adj - popular adjectives for the noun
      /noun - popular nouns for the adjective
      /syn - specific synonyms
      /trigger (tr) - associated words
      /ant - antonyms
      /category (cat) - category (hypernym)
      /specific (spec) - specific items in a category (hyponym)
      /whole - holonym
      /part - meronym
      /next - popular next words
      /prev - popular previous words
      /rhyme (rhy)
      /aprhyme (apr) - approximate rhyme (forest/chorus)
      /homophone (hp) - sounds alike with different spellings (course, coarse)
      /cons - same consonents (sample/simple)

  Examples:
    very difficult - means 'very difficult'
    /means nice /sp b* - means nice, spelling starts with 'b'
    /means nice /spell betr - means nice, spells like 'betr'
    /means nice /so betr - means nice, sounds like 'betr'
    /rhy nice - rhymes with 'nice'
  '''
  all_switches = [\
  {"switch":"means", "short":"m", "urlparam":"ml"}, \
  {"switch":"spell", "short":"sp", "urlparam":"sp"}, \
  {"switch":"sounds", "short":"sou", "urlparam":"sl"}, \
  {"switch":"topics", "short":"_", "urlparam":"topics"}, \
  {"switch":"dict", "short":"_", "urlparam":"md", "mdflag":"d"}, \
  {"switch":"freq", "short":"_", "urlparam":"md", "mdflag":"f"}, \
  {"switch":"pron", "short":"_", "urlparam":"md", "mdflag":"r", "extraparam":"ipa=1"}, \
  {"switch":"adj", "short":"_", "urlparam":"rel_jjb"}, \
  {"switch":"noun", "short":"_", "urlparam":"rel_jja"}, \
  {"switch":"syn", "short":"_", "urlparam":"rel_syn"}, \
  {"switch":"trigger", "short":"tr", "urlparam":"rel_trg"}, \
  {"switch":"ant", "short":"_", "urlparam":"rel_ant"}, \
  {"switch":"category", "short":"cat", "urlparam":"rel_spc"}, \
  {"switch":"specific", "short":"spec", "urlparam":"rel_gen"}, \
  {"switch":"whole", "short":"_", "urlparam":"rel_par"}, \
  {"switch":"part", "short":"_", "urlparam":"rel_com"}, \
  {"switch":"next", "short":"_", "urlparam":"rel_bga"}, \
  {"switch":"prev", "short":"_", "urlparam":"rel_bgb"}, \
  {"switch":"rhyme", "short":"rhy", "urlparam":"rel_rhy"}, \
  {"switch":"aprhyme", "short":"apr", "urlparam":"rel_nry"}, \
  {"switch":"homophone", "short":"hp", "urlparam":"rel_hom"}, \
  {"switch":"cons", "short":"_", "urlparam":"rel_cns"} \
  ]

  @classmethod
  def get_default_switch(cls, word = ""):
    return cls.get_switch("means", word)

  @classmethod
  def get_switch(cls, name, word = ""):
    switch = None
    if (name != ""):
      switch = next((item for item in cls.all_switches if ((item["switch"] == name) or (item["short"] != "_" and item["short"] == name))), None)
    if switch != None:
      switch = copy.deepcopy(switch)
      switch["word"] = word
    return switch


class DataMuseLookup(LookupStrategy):
  switch_char = '/'

  @classmethod
  def process_tags(cls, entry):
    e = entry["word"]
    if ("tags" in entry):
      p = next((item.split(":")[1] for item in entry["tags"] if (item.startswith("ipa_pron"))), None)
      if p != None:
        e += (" (" + p + ")")
      p = next((item.split(":")[1] for item in entry["tags"] if (item.startswith("f:"))), None)
      if p != None:
        e += (", f=" + p)
    return e

  @classmethod
  def extract_data(cls, data):
    result = []
    for x in data:
      if ("score" not in x):
        x["score"] = 0
    sorted_data = sorted(data, key = lambda x : x["score"], reverse = True)
    defs_present = False
    for entry in sorted_data:
        e = [cls.process_tags(entry)]
        if "defs" in entry:
            top = ["","",""]
            i = 0
            for d in entry["defs"][:3]:
              e.append(d.replace("\t", " "))
              defs_present = True
        result.append(e)
    #if defs were present, update all result entries to have three def
    #elements to play nice with Sublime's quick panel
    if defs_present:
        for e in result:
            l = len(e);
            d = 4-l
            while l < 4:
                e.append("");
                l += 1;
    #result = [["test", "expl"],["1", "2", "3"]]
    return result

  @classmethod
  def extract_switches_from_text(cls, text):
    l = list(map(str.strip, text.split(None, 1)))
    ll = len(l)
    if (ll < 1):
      return None
    elif (ll == 1):
      return DataMuseCommandSwitches.get_switch(l[0]);
    else:
      return DataMuseCommandSwitches.get_switch(l[0], l[1]);

  @classmethod
  def get_url(cls, word, language):
    _word = word.strip()
    switches = []
    if _word[0] != cls.switch_char:
      #no command, take the first word and apply default switch
      switch = DataMuseCommandSwitches.get_default_switch(_word)
      if switch != None:
        switches.append(switch)
    else:
      words = list(map(str.strip, _word.split(cls.switch_char)))
      #pop out the first empty string
      if words[0] == "":
        words.pop(0)
      if len(words) < 1:
        #no useful text
        return None
      else:
        for x in words:
          switch = cls.extract_switches_from_text(x)
          if switch != None:
            switches.append(switch)
    url = "https://api.datamuse.com/words"
    url_joiner = '?'
    mdflags = ""
    lastflags = ""
    for switch in switches:
      urlparam = switch["urlparam"]
      if (urlparam == "md"):
        mdf = switch["mdflag"]
        if (mdf == 'r'):
          lastflags = "ipa=1"
        mdflags += switch["mdflag"]
      else:
        url += (url_joiner + urlparam)
        if (switch["word"] != ""):
          url += ("=" + quote(switch["word"]))
        url_joiner = '&'
    if (mdflags != ""):
      url += (url_joiner + "md=" + mdflags)
    if lastflags != "":
      url += (url_joiner + lastflags)
    print(url)
    return url

class ReplaceCommand(sublime_plugin.TextCommand):
  def run(self, edit, region_a, region_b, replacement_text):
    self.view.replace(edit, sublime.Region(region_a, region_b), replacement_text)

class ThesaurusCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.result = []
    self.region = False
    self.value = ""
    self.edit = edit
    if self.data_source() == "datamuse":
      self.lookup_strategy = DataMuseLookup
    else:
      self.lookup_strategy = AlterVistaLookup

    # process our selected word
    self.processWord(self.selected_word())

  def noAction(self, value):
    self.view.erase_status("Thesaurus")
    pass

  def processWord(self, word):
    self.word = word
    if self.word is None or len(self.word) == 0:
      self.view.set_status("Thesaurus", "Please select a word first!")
      sublime.active_window().show_quick_panel(["Please select a word first!"], self.noAction)
      return

    try:
      self.results = self.lookup_strategy.synonyms(self.word, self.language())
      sublime.active_window().show_quick_panel(self.results, self.valueIsSelected)
    except NoResultError as e:
      # nothing was found, look for alternatives
      print(str(e))
      if (str(e) == "\'error\'"):
        self.view.set_status("Thesaurus", "Error retrieving related words for '%s'!" % self.word)
      else:
        self.view.set_status("Thesaurus", "No results were found for '%s'!" % self.word)
      self.alternatives = ["No results were found for '%s'!, try one of the following:" % self.word]
      self.alternatives.extend(self.get_alternative_words())
      sublime.active_window().show_quick_panel(self.alternatives, self.alternativeIsSelected)

  def alternativeIsSelected(self, value):
    if value > 1:
      self.processWord(self.alternatives[value])
    else:
      self.view.erase_status("Thesaurus")

  def valueIsSelected(self, value):
    if value != -1:
      self.replace(self.results[value])
      self.view.erase_status("Thesaurus")

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
      self.view.run_command("replace", {"region_a":self.region.a,"region_b":self.region.b,"replacement_text":value.strip().lower()})

  def data_source(self):
    settings = sublime.load_settings('Thesaurus.sublime-settings')
    if settings.get("data_source"):
      return settings.get("data_source")
    else:
      settings = sublime.load_settings('Preferences.sublime-settings')
      return settings.get("thesaurus_data_source")

  def language(self):
    settings = sublime.load_settings('Thesaurus.sublime-settings')
    if settings.get("language"):
      return settings.get("language")
    else:
      settings = sublime.load_settings('Preferences.sublime-settings')
      return settings.get("thesaurus_language")

  def get_alternative_words(self):
    # dirty hack around not being able to use enchant in sublime
    import subprocess
    try:
      p = subprocess.Popen(["python", alternativesLocation, self.word], stdout=subprocess.PIPE)
      alternativesString = p.communicate()[0]
      p.stdout.close()
      alternatives = []
      # this will replace the alternatives var
      exec(alternativesString)
    except Exception as err:
      alternatives = ['error', str(err)]
      print(alternatives)
    if ((len(alternatives) > 0) and (alternatives[0] == "error")):
      print("Enchant error: %s, defaulting to dummy method..." % alternatives[1])
      # nope, an error occurred, do it the dummy way
      suffixes = ["es", "s", "ed", "er", "ly", "ing"]
      alternatives = []
      for suffix in suffixes:
        if self.word.endswith(suffix):
          alternatives.append(self.word[:(-1*len(suffix))]);
    return alternatives
