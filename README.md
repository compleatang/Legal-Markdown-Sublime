# Introduction

This package is a set of commands to help build legal documents in Sublime. It is opinionated in that I prefer to use [Pandoc](http://johnmacfarlane.net/pandoc/), along with my [Legal Markdown Gem](https://github.com/compleatang/legal-markdown). I use the Gem as a prepocessor and Pandoc as a post processor. To make it easier for those who may not want to install the gem, the ruby files have been extracted into the package as standalone ruby files. 

# Dependencies

You will need to have both pandoc installed and in your PATH for this Package to work fully. You will also need ruby on your system. 

# Using

## Step 1 - Build the YAML Front Matter

The Package assists you to build legal document templates using optional clauses, mixins, and structured headers according to the format established in the `legal_markdown` [gem](https://github.com/compleatang/legal-markdown). 

I find this a lifesaver on long templates -- particularly when I've changed some of the provisions deep in the document. To build the YAML Front Matter simply open Command Pallette and find "Make YAML Front Matter". That's it. I currently have a default key binding of `ctrl+shift+l` followed by `ctrl+shift+y` that will also run the command. 

## Step 2 - Parse Legal Markdown to Create Normal Markdown

After you have worked on your template, forked it or whatever, you can easily parse the legal markdown to create normal markdown. To use this function open Command Pallete and find "Legal Markdown to Normal Markdown". You can also use the default key binding of `ctrl+shift+l` followed by `ctrl+shift+b` which will also run the command (or any other key binding you set in your User directory).

# Installation

<!-- ## Install using Sublime Package Control

If you are using Will Bond's excellent Sublime Package Control, you can easily install Paste PDF via the Package Control: Install Package menu item. The Paste PDF package is listed there. See "Package Control" http://wbond.net/sublime_packages/package_control -->

## Install using Git

You can install the theme and keep up to date by cloning the repo directly into your Packages directory in the Sublime Text 2 application settings area. You can locate your Sublime Text 2 Packages directory by using the menu item Preferences -> Browse Packages. While inside the Packages directory, clone the theme repository using the command below:

```
$ git clone https://github.com/compleatang/Legal-Markdown-Sublime.git
```

## Manual Install

To download and install package manually:

* Download the files using the GitHub .zip download option
* Unzip the files and rename the folder to Paste PDF
* Move the folder to your Sublime Text 2 Packages directory

# Contributing

PLEASE! Feel free to add your snippets. This will be helpful to the community of lawyers using Sublime. To contribute do the following.

1. From your Sublime Packages folder you'll want to clone the repository by typing `git clone git@github.com:compleatang/Legal-Markdown-Sublime.git`.
2. In Github you'll want to fork this repository to your account. Do this by pressing the "Fork" button at the top left of this repository.
3. Next type (from the folder where your repository sits) `git remote add myfork git@github.com:[YOUR USERNAME]/Legal-Markdown-Sublime.git`.
4. Then you are all set to add any snippets you may want.

When you have added a new file then simply commit that code, push to your fork on your Github and then send a pull request.

# [Source Code](https://github.com/compleatang/Legal-Markdown-Sublime)

MIT License - (c) 2013 - Watershed Legal Services, PLLC

# TODO / Roadmap

- [X] Integrate function to automatically build YAML frontmatter.
- [X] Integrate Gem functionality to render the legal markdown to full markdown.
- [ ] Syntax highlighting by forking SmartMarkdown's Template and/or making a .lmd tmlanguage.  l. - as Constants; ll. - as def's; mixins - as keywords (def, if, etc.); clauses - as strings; yaml - as yaml syntax already is...
- [ ] Integrate Pandoc.
- [ ] Keymapings for `...?ASK?...` and `...?CONFIRM?...`
- [ ] Form a checklist from questions in template
