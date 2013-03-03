# Introduction

This package is (going to be) a set of snippets and commands to help build legal documents in Sublime. It is opinionated in that I prefer to use [Pandoc](http://johnmacfarlane.net/pandoc/), along with my [Legal Markdown Gem](https://github.com/compleatang/legal-markdown). That said, the snippets should work just fine for any set up you may have. The snippets are currently scoped for markdown files (not multimarkdown). That means they will not work in other syntaxes. If you open a document and want to use the snippets, simply change your syntax for that file to markdown by going to View -> Syntax -> Markdown. If you have MultiMarkdown installed you'll have a submenu under Markdown, select Markdown from there.

At this point I've only a sample snippet as I haven't yet had time to do much on this package. I plan to have snippets built into three folders: Contracts Snippets, Filings Snippets, Policy Snippets. 

# Using

Very simple. From a markdown file just open the command pallette, type Snippet and whatever you're looking for, then hit enter and voila it should be there. 

# Installation

<!-- ## Install using Sublime Package Control

If you are using Will Bond's excellent Sublime Package Control, you can easily install Paste PDF via the Package Control: Install Package menu item. The Paste PDF package is listed there. See "Package Control" http://wbond.net/sublime_packages/package_control -->

## Install using Git

You can install the theme and keep up to date by cloning the repo directly into your Packages directory in the Sublime Text 2 application settings area. You can locate your Sublime Text 2 Packages directory by using the menu item Preferences -> Browse Packages. While inside the Packages directory, clone the theme repository using the command below:

```
$ git clone https://github.com/compleatang/sublimetext-pastepdf
```

## Manual Install

To download and install package manually:

* Download the files using the GitHub .zip download option
* Unzip the files and rename the folder to Paste PDF
* Move the folder to your Sublime Text 2 Packages directory

# Contributing

PLEASE! Feel free to add your snippets. This will be helpful to the community of lawyers using Sublime. To contribute do the following.

    1. From your Sublime Packages folder you'll want to clone the repository by typing `git clone git@github.com:compleatang/Legally-Sublime.git`.
    2. In Github you'll want to fork this repository to your account. Do this by pressing the "Fork" button at the top left of this repository.
    3. Next type (from the folder where your repository sits) `git remote add myfork git@github.com:[YOUR USERNAME]/Legally-Sublime.git`.
    4. Then you are all set to add any snippets you may want.

Please add your snippets to the appropriate folder. Snippet files are easy to create by simply duplicating the template files and changing what you want (or changing my text to suit your practice). 

When you have added a new file (or updated some default text) then simply commit that code, push to your fork on your Github and then send a pull request. For now I'll probably only pull in snippets that aren't already built. Am open to discussion of the default text, especially where my boilerplate may not suit others. Just drop an Issue in Github Issues for this repository and we can have a chat about it.

# [Source Code](https://github.com/compleatang/Legally-Sublime)

MIT License - (c) 2012 - Watershed Legal Services, PLLC

# TODO / Roadmap

[ ] Build syntax highlighting for legal documents that utilize the Gem syntax
[ ] Build more snippets
[ ] Integrate the gem workflow into this Package -- in particular a script that will scrape the document and populate the YAML frontmatter based on the Gem syntax and move the cursor to the top.