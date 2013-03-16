# Introduction

This package is a set of commands to help build legal documents in Sublime. It is opinionated in that I prefer to use [Pandoc](http://johnmacfarlane.net/pandoc/), along with my [Legal Markdown Gem](https://github.com/compleatang/legal-markdown). I use the Gem as a prepocessor and Pandoc as a post processor.

# Dependencies

You will need to have both the gem and pandoc installed and in your PATH for this Package to work properly. See the above links for installing these.

# Using

## Step 1 - Build the YAML Front Matter

The Package will scan your document for optional clauses, mixins, and structured headers according to the Gem format and will automatically populate the YAML front matter for you. I find this a lifesaver on long templates -- particularly when I've changed some of the provisions deep in the document. To build the YAML Front Matter simply open Command Pallette and find Build YAML Front Matter. That's it. I currently have a default key binding of `ctrl+shift+l` for legal that will also run the command. The command is greedy in that it will strip any existing YAML Front Matter you currently have, so be careful using if you've put some unique stuff in the YAML front matter.

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

MIT License - (c) 2012 - Watershed Legal Services, PLLC

# TODO / Roadmap

- [X] Integrate function to automatically build YAML frontmatter.
- [ ] Syntax highlighting by forking SmartMarkdown's Template and/or making a .lmd tmlanguage.
- [ ] Go to mixin in YAML header; go to mixin in the text. l. - as Constants; ll. - as def's; mixins - as keywords (def, if, etc.); clauses - as strings; yaml - as yaml syntax already is...
- [ ] Integrate Gem functionality to render the legal markdown to full markdown.
- [ ] Integrate Pandoc.
- [ ] Keymapings for `...?ASK?...` and `...?CONFIRM?...`
- [ ] Form a checklist from questions in template
