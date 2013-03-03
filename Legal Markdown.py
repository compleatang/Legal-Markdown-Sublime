# coding=utf8
import sublime_plugin, sublime, re, sets

# Build Yaml Front Matter
class BuildYamlFrontMatter(sublime_plugin.TextCommand):
  def run(self, edit):
    selection = sublime.Region(0L, self.view.size())
    result = self.buildYamlFrontMatter(self.view.substr(selection))
    if result:
      self.view.replace(edit, selection, result)

  def buildYamlFrontMatter( self, selection ):
    mixins_pattern = re.compile("\{\{(\S+)\}\}")
    headers_pattern = re.compile("^(l+)\.\s",re.MULTILINE)
    yaml_pattern = re.compile("^(\s*---.*---\s*$)",re.MULTILINE|re.DOTALL)

    yaml = yaml_pattern.findall( selection )
    if yaml:
      selection = selection.replace( yaml[0], '' )

    mixins = mixins_pattern.findall( selection )
    # uniq_mixins  = list(set(mixins)).sort()
    uniq_mixins  = [list(x) for x in set(tuple(x) for x in mixins)]
    uniq_mixins.sort()
    headers = headers_pattern.findall( selection )
    # uniq_headers = list(set(headers)).sort()
    uniq_headers = [list(x) for x in set(tuple(x) for x in headers)]
    uniq_headers.sort()
    new_yaml =  '---\n\n# First, the Mixins\n'
    for mixin in uniq_mixins:
      mixin = ''.join(mixin)
      new_yaml = new_yaml + mixin + ': \n'
    new_yaml = new_yaml + '# Now, for the Headers\n'
    for header in uniq_headers:
      new_yaml = new_yaml + 'level-' + str(header.count('l')) + ': \n'
    new_yaml = new_yaml + '\n---\n'

    selection = new_yaml + selection
    return selection
