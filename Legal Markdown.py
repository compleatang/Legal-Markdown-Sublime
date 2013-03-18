# coding=utf8
import os.path
import sublime, sublime_plugin, sys, re
import subprocess

# Build Yaml Front Matter
class BuildYamlFrontMatter(sublime_plugin.TextCommand):
  def run(self, edit):
    self.settings = sublime.load_settings('LegalMarkdown.sublime-settings')
    self.get_selection_position()
    self.active_view = self.view.window().active_view()
    self.buffer_region = sublime.Region(0, self.active_view.size())
    self.update_view(self.yamlize_buffer())
    self.reset_selection_position()

  def yamlize_buffer(self):
    working_dir = os.path.dirname(self.view.file_name())
    body = self.active_view.substr(self.buffer_region)
    yamlizer = subprocess.Popen(self.cmd(), shell=True, cwd=working_dir, 
      stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = yamlizer.communicate(body.encode("utf-8"))[0].decode('utf8')
    if (out == "" and body != ""):
      sublime.error_message("check your ruby interpreter settings")
      return body
    else:
      return out

  def update_view(self, contents):
    edit = self.view.begin_edit()
    self.view.erase(edit, self.buffer_region)
    self.view.insert(edit, 0, contents)
    self.view.end_edit(edit)

  def reset_selection_position(self):
    self.view.sel().clear()
    self.view.sel().add(self.region)
    self.view.show(self.view.text_point(0, 0))

  def get_selection_position(self):
    sel         = self.view.sel()[0].begin()
    pos         = self.view.rowcol(sel)
    target      = self.view.text_point(pos[0], 0)
    self.region = sublime.Region(target)

  def cmd(self, path = "-"):
    ruby_interpreter = self.settings.get('ruby') or "/usr/bin/env ruby"
    ruby_script = os.path.join(sublime.packages_path(), "Legal Markdown", 'lib', 'legal_markdown.rb')
    args = [ "--headers", "'" + unicode(path) + "'"]
    command = ruby_interpreter + " '" + ruby_script + "' " + ' '.join(args)
    return command

class LegalMarkdownToNormalMarkdown(sublime_plugin.WindowCommand):
  def run(self):
    self.settings = sublime.load_settings('LegalMarkdown.sublime-settings')
    self.active_view = self.window.active_view()
    self.buffer_region = sublime.Region(0, self.active_view.size())
    self.window.show_input_panel("Save to:", str(self.get_current_file()), 
      self.on_input, None, None)

  def on_input(self, output_file):
    output_file = str(output_file)
    working_dir = os.path.dirname(self.get_current_file())
    body = self.active_view.substr(self.buffer_region)
    mdizr = subprocess.Popen(self.cmd(output_file), shell=True, cwd=working_dir, 
      stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = mdizr.communicate(body.encode("utf-8"))[0].decode('utf8')
    if (out != "" and body != ""):
      sublime.error_message("Check your legal markdown file.")
    else:
      self.window.open_file(output_file)

  def cmd(self, output_file):
    ruby_interpreter = self.settings.get('ruby') or "/usr/bin/env ruby"
    ruby_script = os.path.join(sublime.packages_path(), "Legal Markdown", 'lib', 'legal_markdown.rb')
    args = ["-", "'" + output_file + "'"]
    command = ruby_interpreter + " '" + ruby_script + "' " + ' '.join(args)
    return command

  def get_current_file(self):
    view = self.window.active_view()
    if view and view.file_name() and len(view.file_name()) > 0:
        return view.file_name()
