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
      # return output_file

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

#   def run(self):
#     self.get_window().show_input_panel("Legal Markdown", "",
#         self.on_input, None, None)

#   def on_input(self, command):
#     command = str(command)  # avoiding unicode
#     import shlex
#     command_splitted = ['legal2md'] + shlex.split(command)
#     print command_splitted
#     self.run_command(command_splitted)

#   def get_window(self):
#       return sublime.active_window()

#   def run_command(self, command, filter_empty_args=True, **kwargs):
#       if filter_empty_args:
#           command = [arg for arg in command if arg]
#       if 'working_dir' not in kwargs:
#           kwargs['working_dir'] = self.get_working_dir()
#       if 'fallback_encoding' not in kwargs and self.active_view() and self.active_view().settings().get('fallback_encoding'):
#           kwargs['fallback_encoding'] = self.active_view().settings().get('fallback_encoding').rpartition('(')[2].rpartition(')')[0]

#       thread = CommandThread(command, callback, **kwargs)
#       thread.start()

#       message = kwargs.get('status_message', False) or ' '.join(command)
#       sublime.status_message(message)

#   @property
#   def fallback_encoding(self):
#       if self.active_view() and self.active_view().settings().get('fallback_encoding'):
#           return self.active_view().settings().get('fallback_encoding').rpartition('(')[2].rpartition(')')[0]

#   def get_working_dir(self):
#       file_name = self._active_file_name()
#       if file_name:
#           return os.path.realpath(os.path.dirname(file_name))
#       else:
#           try:  # handle case with no open folder
#               return self.window.folders()[0]
#           except IndexError:
#               return ''

#   def _active_file_name(self):
#       view = self.active_view()
#       if view and view.file_name() and len(view.file_name()) > 0:
#           return view.file_name()

# class CommandThread(threading.Thread):
#     def __init__(self, command, on_done, working_dir="", fallback_encoding="", **kwargs):
#         threading.Thread.__init__(self)
#         self.command = command
#         self.on_done = on_done
#         self.working_dir = working_dir
#         if "stdin" in kwargs:
#             self.stdin = kwargs["stdin"]
#         else:
#             self.stdin = None
#         if "stdout" in kwargs:
#             self.stdout = kwargs["stdout"]
#         else:
#             self.stdout = subprocess.PIPE
#         self.fallback_encoding = fallback_encoding
#         self.kwargs = kwargs

#     def run(self):
#         try:

#             # Ignore directories that no longer exist
#             if os.path.isdir(self.working_dir):

#                 # Per http://bugs.python.org/issue8557 shell=True is required to
#                 # get $PATH on Windows. Yay portable code.
#                 shell = os.name == 'nt'
#                 if self.working_dir != "":
#                     os.chdir(self.working_dir)

#                 proc = subprocess.Popen(self.command,
#                     stdout=self.stdout, stderr=subprocess.STDOUT,
#                     stdin=subprocess.PIPE,
#                     shell=shell, universal_newlines=True)
#                 output = proc.communicate(self.stdin)[0]
#                 if not output:
#                     output = ''
#                 # if sublime's python gets bumped to 2.7 we can just do:
#                 # output = subprocess.check_output(self.command)
#                 main_thread(self.on_done,
#                     _make_text_safeish(output, self.fallback_encoding), **self.kwargs)

#         except subprocess.CalledProcessError, e:
#             main_thread(self.on_done, e.returncode)
#         except OSError, e:
#             if e.errno == 2:
#                 main_thread(sublime.error_message, "Legal Markdown binary could not be found in PATH\n\nPATH is: %s" % os.environ['PATH'])
#             else:
#                 raise e


    # selection = sublime.Region(0L, self.view.size())
    # result = self.buildYamlFrontMatter(self.view.substr(selection))
    # if result:
    #   self.view.replace(edit, selection, result)

    # ==================================

  # def buildYamlFrontMatter( self, selection ):
  #   clauses_pattern = re.compile("\[\{\{(\S+)\}\}")
  #   mixins_pattern = re.compile("[^\[]\{\{(\S+)\}\}")
  #   headers_pattern = re.compile("^(l+)\.\s",re.MULTILINE)
  #   yaml_pattern = re.compile("^(\s*---.*---\s*$)",re.MULTILINE|re.DOTALL)

  #   yaml = yaml_pattern.findall( selection )
  #   if yaml:
  #     selection = selection.replace( yaml[0], '' )

  #   clauses = clauses_pattern.findall( selection )
  #   uniq_clauses  = [list(x) for x in set(tuple(x) for x in clauses)]
  #   uniq_clauses.sort()
    
  #   mixins = mixins_pattern.findall( selection )
  #   uniq_mixins  = [list(x) for x in set(tuple(x) for x in mixins)]
  #   uniq_mixins.sort()

  #   headers = headers_pattern.findall( selection )
  #   uniq_headers = [list(x) for x in set(tuple(x) for x in headers)]
  #   uniq_headers.sort()

  #   if len(uniq_clauses) == 0 and len(uniq_mixins) == 0 and len(uniq_headers) == 0:
  #     return selection

  #   new_yaml =  '---\n'

  #   if len(uniq_clauses) != 0:
  #     new_yaml += '\n# Optional Clauses\n'
  #   for clause in uniq_clauses:
  #     clause = ''.join(clause)
  #     new_yaml += clause + ': \n'

  #   if len(uniq_mixins) != 0:
  #     new_yaml += '\n# Mixins\n'
  #   for mixin in uniq_mixins:
  #     mixin = ''.join(mixin)
  #     new_yaml += mixin + ': \n'

  #   if len(uniq_headers) != 0:
  #     new_yaml += '\n# Structured Headers\n'
  #   for header in uniq_headers:
  #     new_yaml += 'level-' + str(header.count('l')) + ': \n'
  #   new_yaml += '\n---\n'

  #   full_monty = [new_yaml, selection]
  #   return ''.join(full_monty)

  # ==========================

  # def prompt(self, message, default, function, arg1):
  #   import functools
  #   sublime.active_window().run_command('hide_panel');
  #   sublime.active_window().show_input_panel(message.decode('utf-8'), default.decode('utf-8'), functools.partial(function, arg1, True), None, None)

  # def run(
  #         self,
  #         object,
  #         modal = False,
  #         background = False,

  #         refresh_funct_view = False,
  #         refresh_funct_command = False,
  #         refresh_funct_item = False,
  #         refresh_funct_to_status_bar = False,
  #         refresh_funct_title = False,
  #         refresh_funct_no_results = False,
  #         refresh_funct_syntax_file = False
  #         ):

  #   if not refresh_funct_view:
  #     pass
  #   else:
  #     object = Object()
  #     object.command = refresh_funct_command
  #     object.item = SideBarItem(refresh_funct_item, os.path.isdir(refresh_funct_item))
  #     object.to_status_bar = refresh_funct_to_status_bar
  #     object.title = refresh_funct_title
  #     object.no_results = refresh_funct_no_results
  #     object.syntax_file = refresh_funct_syntax_file

  #   debug = False
  #   if debug:
  #     print '----------------------------------------------------------'
  #     print 'GIT:'
  #     print object.command
  #     print 'CWD:'
  #     print object.item.forCwdSystemPath()
  #     print 'PATH:'
  #     print object.item.forCwdSystemName()

  #   failed = False

  #   if sublime.platform() == 'windows':
  #     object.command = map(self.escapeCMDWindows, object.command)

  #   if sublime.platform() is not 'windows' and object.command[0] == 'git':
  #     if path_to_git_unixes != '':
  #       object.command[0] = s.get('path_to_git_unixes')
  #     elif os.path.exists('/usr/local/git/bin'):
  #       object.command[0] = '/usr/local/git/bin/git'

  #   cwd = object.item.forCwdSystemPath()

  #   try:
  #     if sublime.platform() == 'windows':

  #       process = subprocess.Popen(
  #                                 #" ".join(object.command),
  #                                 object.command,
  #                                 cwd=cwd,
  #                                 stdout=subprocess.PIPE,
  #                                 stderr=subprocess.STDOUT,
  #                                 shell=True,
  #                                 universal_newlines=True)
  #     else:
  #       process = subprocess.Popen(
  #                                 object.command,
  #                                 cwd=cwd,
  #                                 stdout=subprocess.PIPE,
  #                                 stderr=subprocess.STDOUT,
  #                                 shell=False,
  #                                 universal_newlines=True)

  #     if background:
  #       if debug:
  #         print 'SUCCESS'
  #         print '----------------------------------------------------------'
  #       return True

  #     stdout, stderr = process.communicate()
  #     SideBarGit.last_stdout = str(stdout).rstrip()
  #     self.last_stdout = str(stdout).rstrip()

  #     stdout = stdout.strip()

  #     if stdout.find('fatal:') == 0 or stdout.find('error:') == 0 or stdout.find('Permission denied') == 0 or stderr:
  #       print 'FAILED'
  #       failed = True
  #     else:
  #       if debug:
  #         print 'SUCCESS'
  #     if stdout:
  #       if debug:
  #         print 'STDOUT'
  #         print stdout
  #     if stderr:
  #       print 'STDERR'
  #       print stderr
  #   except OSError as (errno, strerror):
  #     print 'FAILED'
  #     failed = True
  #     print errno
  #     print strerror
  #     SideBarGit.last_stdout = ''
  #     self.last_stdout = ''
  #   except IOError as (errno, strerror):
  #     print 'FAILED'
  #     failed = True
  #     print errno
  #     print strerror
  #     SideBarGit.last_stdout = ''
  #     self.last_stdout = ''
  #   if debug:
  #     print '----------------------------------------------------------'

  #   try:
  #     object.to_status_bar
  #   except:
  #     object.to_status_bar = False

  #   try:
  #     object.silent
  #     return
  #   except:
  #     pass

  #   if failed:
  #     try:
  #       strerror
  #       if errno == 2:
  #         self.alert(strerror+'\nPossible error:\n'+object.command[0]+' not found on $PATH')
  #       else:
  #         self.alert(strerror)
  #       return False
  #     except:
  #       if not stdout and not stderr:
  #         return False
  #       if stdout.find('Permission denied') == 0 or stdout.find('fatal: The remote end hung up unexpectedly') == 0:
  #         self.alert((stdout or '')+'\n'+(stderr or '')+'\nPossible error:\nssh keys not in .ssh/ directory or keys not opened')
  #       else:
  #         self.alert((stdout or '')+'\n'+(stderr or ''))
  #       return False
  #   else:
  #     if stdout != '' and refresh_funct_view == False and (object.to_status_bar or " ".join(object.command).find('git push') == 0 or stdout.find('nothing to commit') == 0):
  #       self.status(stdout)
  #     else:
  #       if stdout == '' and refresh_funct_view == False:
  #         try:
  #           self.status(object.no_results)
  #         except:
  #           self.status('No output to show')
  #         return True
  #       if stdout == '' and refresh_funct_view != False:
  #         try:
  #           stdout = object.no_results
  #         except:
  #           stdout = 'No output to show'
  #       if stdout == '':
  #         return True

  #       if refresh_funct_view == False:
  #         view = sublime.active_window().new_file()
  #       else:
  #         view = refresh_funct_view
  #       try:
  #         view.set_name(object.title.decode('utf-8'))
  #       except:
  #         view.set_name('No Title')
  #       try:
  #         if object.syntax_file != False:
  #           view.set_syntax_file(object.syntax_file)
  #       except:
  #         pass
  #       try:
  #         object.word_wrap
  #         view.settings().set('word_wrap', False)
  #       except:
  #         pass
  #       view.settings().set('fallback_encoding', 'UTF-8')
  #       view.settings().set('encoding', 'UTF-8')
  #       view.settings().set('default_dir', object.item.dirname())
  #       view.set_scratch(True)

  #       if refresh_funct_view == False:
  #         view.settings().set('SideBarGitIsASideBarGitTab', True)
  #         view.settings().set('SideBarGitCommand', object.command)
  #         view.settings().set('SideBarGitModal', modal)
  #         view.settings().set('SideBarGitBackground', background)
  #         view.settings().set('SideBarGitItem', object.item.path())
  #         try:
  #           view.settings().set('SideBarGitToStatusBar', object.to_status_bar)
  #         except:
  #           view.settings().set('SideBarGitToStatusBar', False)
  #         try:
  #           view.settings().set('SideBarGitTitle', object.title)
  #         except:
  #           view.settings().set('SideBarGitTitle', 'No Title')
  #         try:
  #           view.settings().set('SideBarGitNoResults', object.no_results)
  #         except:
  #           view.settings().set('SideBarGitNoResults', 'No output to show')
  #         try:
  #           view.settings().set('SideBarGitSyntaxFile', object.syntax_file)
  #         except:
  #           view.settings().set('SideBarGitSyntaxFile', False)

  #       content = "[SideBarGit@SublimeText "
  #       content += object.item.name().decode('utf-8')
  #       content += "/] "
  #       content += (" ".join(object.command)).decode('utf-8')
  #       content += "\n\n"
  #       content += "# Improve this command, the output or the tab title by posting here:"
  #       content += "\n"
  #       content += "# http://www.sublimetext.com/forum/viewtopic.php?f=5&t=3405"
  #       content += "\n"
  #       content += "# Tip: F5 will run the command again and refresh the contents of this tab"
  #       content += "\n\n"
  #       try:
  #         content += stdout
  #       except:
  #         content += unicode(stdout, 'UTF-8', errors='ignore')

  #       edit = view.begin_edit()
  #       view.replace(edit, sublime.Region(0, view.size()), content);
  #       view.sel().clear()
  #       view.sel().add(sublime.Region(0))
  #       view.end_edit(edit)
  #   return True
