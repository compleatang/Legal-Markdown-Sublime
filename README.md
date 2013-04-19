# Introduction

This package is meant to help build legal documents in Sublime. There are two components of the package at this point. The first is a set of language files for syntax highlighting `lmd` files in Sublime. The second is a set of features to build and export documents using `lmd` syntax. This set of features will:

* Automate the building of the `lmd` YAML Front Matter
* Build `lmd` files to regular `md`
* Build `lmd` files to any format Pandoc handles. 

The package is opinionated in that I prefer to use [Pandoc](http://johnmacfarlane.net/pandoc/), along with my [Legal Markdown Gem](https://github.com/compleatang/legal-markdown) to forumlate documents using the full range of pandoc's features. The package uses the Gem as a prepocessor and Pandoc as the primary processor. To make it easier for those who may not want to install the gem, the ruby files have been extracted into the package as standalone ruby files so there is no need to install the gem if you simply include the package. Indeed the package will rely upon the ruby files included and will not call the gem even if you have it installed on your system. 

If you do not want to use pandoc you can still use the rest of the package without any problem, if you have ruby on your system.

# Dependencies

You will need to have both ruby and pandoc installed and in your PATH for this Package to work fully. If you have a non-standard ruby or pandoc install, for instance if you have installed pandoc from cabal, then just type `which pandoc` to the command line and copy the output (without the pandoc portion) to the `pandoc-path` in your User Settings for the Legal Markdown package (Preferences->Package Settings->Legal Markdown->Settings - User). Similarly for ruby, but if you have used rvm or have a system installed ruby it should work fine. 

# Using

## Step 1 - Build the YAML Front Matter

The Package assists you to build legal document templates using optional clauses, mixins, and structured headers according to the format established in the `legal_markdown` [gem](https://github.com/compleatang/legal-markdown). 

I find this a lifesaver on long templates -- particularly when I've changed some of the provisions deep in the document. To build the YAML Front Matter simply open Command Pallette and find "Legal Markdown - Make YAML Front Matter". That's it. I currently have a default key binding of `ctrl+shift+l` followed by `ctrl+shift+y` that will also run the command. 

## Step 2a - Parse Legal Markdown to Create Normal Markdown

After you have worked on your template, forked it or whatever, you can easily parse the legal markdown to create normal markdown. To use this function open Command Pallete and find "Legal Markdown - Convert to Normal Markdown". You can also use the default key binding of `ctrl+shift+l` followed by `ctrl+shift+m` which will also run the command (or any other key binding you set in your User directory). I love using this in combination with the very nice [Markdown Preview Package](https://github.com/revolunet/sublimetext-markdown-preview) to view `lmd` files in my browser. This is great when you want to read laws, etc.

## Step 2b - Parse Legal Markdown to Create a DOCX, ODT, PDF, etc. with Pandoc

This package integrates Pandoc. The way I have integrated pandoc is slightly different than other pandoc integrations for Sublime. The other integrations are perfectly competent for their purposes, but I wanted to build something that was more tightly integrated. 

The philosophy of this package's pandoc integration is to define document types (client memos, internal research memos, transactional contracts, corporate governance, whatever you use) in the settings and then when you want to export a `lmd` file just to select that document type. So here's how you do that.

Go to Preferences -> Package Settings -> Legal Markdown -> Settings - Default. Copy over the format for the `build-format` block. Then go to Preferences -> Package Settings -> Legal Markdown -> Settings - User and paste the block inside the settings file. Then you can build the Document Types however you want. An explanation is below (you can also just paste the below into your user settings file if you prefer.)

```json
"build-formats": {
    "Memo": {                                                   // Name of the Document Type
      "from": ["markdown+fancy_lists+startnum"],                // The pandoc reader options ... note this is pandoc 1.10+ format so be careful using +/-
      "to": ["odt", "--reference-odt", "~/.pandoc/memo.odt"],   // The pandoc writer options
      "options": ["-S", "--normalize"],                         // The pandoc general options
      "file-output": "true",                                    // Use if you want to output to a file, or use the pandoc -o flag
      "open-file-after-build": "libreoffice"                    // Command to open the document with. Delete field if you don't want to automatically open the file.
    }
}
``` 

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
- [X] Syntax highlighting for `lmd` language.
- [X] Integrate Pandoc.
- [ ] Keymapings for `...?ASK?...` and `...?CONFIRM?...`
- [ ] Form a checklist from questions in template
