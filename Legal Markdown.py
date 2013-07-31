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
    ruby_interpreter = self.settings.get('ruby-path') or "/usr/bin/env ruby"
    ruby_script = os.path.join(sublime.packages_path(), "Legal Document Creator", "lib", 'legal_markdown.rb')
    args = ["--headers", "-", "-"]
    command = ruby_interpreter + " '" + ruby_script + "' " + ' '.join(args)
    print command
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
    ruby_interpreter = self.settings.get('ruby-path') or "/usr/bin/env ruby"
    ruby_script = os.path.join(sublime.packages_path(), "Legal Document Creator", "lib", 'legal_markdown.rb')
    args = ["-", "'" + output_file + "'"]
    command = ruby_interpreter + " '" + ruby_script + "' " + ' '.join(args)
    return command

  def get_current_file(self):
    view = self.window.active_view()
    if view and view.file_name() and len(view.file_name()) > 0:
        return view.file_name()

class LegalMarkdownExport(sublime_plugin.WindowCommand):

    def run(self):
        self.active_view = self.window.active_view()
        self.buffer_region = sublime.Region(0, self.active_view.size())
        self.window.show_quick_panel(self.get_the_settings('build-formats').keys(), self.build_new_format)

    def build_new_format(self, format_to):
        formats = self.get_the_settings('build-formats')
        if format_to == -1:
            return
        format_to = formats[formats.keys()[format_to]]
        view = self.window.active_view()

        # string to work with
        contents = self.mdizer(self.active_view.substr(self.buffer_region))

        # pandoc params
        command = [self.find_binary('pandoc')]
        # configured options
        if 'options' in format_to:
            command.extend(format_to['options'])
        if 'from' in format_to:
            command.extend(['-f'])
            command.extend(format_to['from'])
        if 'to' in format_to:
            command.extend(['-t'])
            command.extend(format_to['to'])
        # if output file
        output_file = False
        if format_to['file-output'] == 'true':
            output_file = os.path.splitext(sublime.Window.active_view(sublime.active_window()).file_name())[0]
            output_file_name =  '"' + output_file + "." + format_to['to'][0] + '"'
            command.extend(['-o', output_file_name])
        # final build
        command = ' '.join(command)

        # run pandoc
        # sublime.message_dialog(command)
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if contents:
            result, error = process.communicate(contents.encode('utf-8'))
        else:
            contents = self.active_view.substr(self.buffer_region)
            result, error = process.communicate(contents.encode('utf-8'))

        # replace buffer and set syntax
        if output_file:
            if format_to['open-file-after-build'] and format_to['open-file-after-build'] != 'false':
                open_command = [format_to['open-file-after-build'], output_file_name]
                open_command = ' '.join(open_command)
                subprocess.Popen(open_command, shell=True)
            else:
                sublime.message_dialog('Wrote to file ' + output_file_name)
        else:
            if result:
                edit = view.begin_edit()
                view.replace(edit, region, result)
                if 'syntax_file' in format_to:
                    view.set_syntax_file(format_to['syntax_file'])
                view.end_edit(edit)
            if error:
                sublime.error_message(error)

    def get_the_settings(self, key):
        return sublime.load_settings('LegalMarkdown.sublime-settings').get(key)

    def find_binary(self, name):
        if self.get_the_settings('pandoc-path') is not None:
            return os.path.join(self.get_the_settings('pandoc-path'), name)
        # Try the path first
        for dir in os.environ['PATH'].split(os.pathsep):
            path = os.path.join(dir, name)
            if os.path.exists(path):
                return path
        dirs = ['/usr/local/bin', '/usr/bin']
        for dir in dirs:
            path = os.path.join(dir, name)
            if os.path.exists(path):
                return path
        return None

    def mdizer(self, contents):
        ruby_interpreter = os.path.join(self.get_the_settings('ruby-path')) or "/usr/bin/env ruby"
        ruby_script = os.path.join(sublime.packages_path(), "Legal Document Creator", "lib", 'legal_markdown.rb')
        args = ["-", "-"]
        md_command = ruby_interpreter + " '" + ruby_script + "' " + ' '.join(args)
        mdizr = subprocess.Popen(md_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out = mdizr.communicate(contents.encode("utf-8"))[0].decode('utf8')
        return out
