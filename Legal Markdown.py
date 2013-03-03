# coding=utf8
import sublime_plugin, sublime, re

# Build Yaml Front Matter
class BuildYamlFrontMatter(sublime_plugin.TextCommand):
  def run(self, edit):
    selection = sublime.Region(0L, self.view.size())
    result = self.buildYamlFrontMatter(self.view.substr(selection))
    if result:
      self.view.replace(edit, selection, result)

  def buildYamlFrontMatter( self, selection ):
    clauses_pattern = re.compile("\[\{\{(\S+)\}\}")
    mixins_pattern = re.compile("\{\{(\S+)\}\}\s")
    headers_pattern = re.compile("^(l+)\.\s",re.MULTILINE)
    yaml_pattern = re.compile("^(\s*---.*---\s*$)",re.MULTILINE|re.DOTALL)

    yaml = yaml_pattern.findall( selection )
    if yaml:
      selection = selection.replace( yaml[0], '' )

    clauses = clauses_pattern.findall( selection )
    uniq_clauses  = [list(x) for x in set(tuple(x) for x in clauses)]
    uniq_clauses.sort()
    
    mixins = mixins_pattern.findall( selection )
    uniq_mixins  = [list(x) for x in set(tuple(x) for x in mixins)]
    uniq_mixins.sort()

    headers = headers_pattern.findall( selection )
    uniq_headers = [list(x) for x in set(tuple(x) for x in headers)]
    uniq_headers.sort()

    if len(uniq_clauses) == 0 and len(uniq_mixins) == 0 and len(uniq_headers) == 0:
      return selection

    new_yaml =  '---\n'

    if len(uniq_clauses) != 0:
      new_yaml += '\n# Optional Clauses\n'
    for clause in uniq_clauses:
      clause = ''.join(clause)
      new_yaml += clause + ': \n'

    if len(uniq_mixins) != 0:
      new_yaml += '\n# Mixins\n'
    for mixin in uniq_mixins:
      mixin = ''.join(mixin)
      new_yaml += mixin + ': \n'

    if len(uniq_headers) != 0:
      new_yaml += '\n# Structured Headers\n'
    for header in uniq_headers:
      new_yaml += 'level-' + str(header.count('l')) + ': \n'
    new_yaml += '\n---\n'

    full_monty = [new_yaml, selection]
    return ''.join(full_monty)
