---
type: "post"
aliases:
- /2012/08/html-and-xhtml-built-in-support-in-vim.html
date: "2012-08-20T00:00:00Z"
tags:
- linux
- fedora
- vim
title: HTML and XHTML built in support in Vim
---

For some reason, everytime I read something about Vim and (X)HTML support,
guys are referring to many weird plugins and extra tools, which is often
outdated.

Many folks do not know, that Vim 7+ has **decent support for XML/XHTML/HTML
languages** (**no plugins needed**!) with possibilities to extend it with any
XML-based language you want. What you can do is to use DTD/RNG converters that
prepares Vim definition which is used to give you omni completion.

For example, my Vim installation contains support for HTML4 and XHTML
languages by default:

        $ rpm -ql vim vim-common | grep xml
        /usr/share/vim/vim73/autoload/xml
        /usr/share/vim/vim73/autoload/xml/html32.vim
        /usr/share/vim/vim73/autoload/xml/html401f.vim
        /usr/share/vim/vim73/autoload/xml/html401s.vim
        /usr/share/vim/vim73/autoload/xml/html401t.vim
        /usr/share/vim/vim73/autoload/xml/html40f.vim
        /usr/share/vim/vim73/autoload/xml/html40s.vim
        /usr/share/vim/vim73/autoload/xml/html40t.vim
        /usr/share/vim/vim73/autoload/xml/xhtml10f.vim
        /usr/share/vim/vim73/autoload/xml/xhtml10s.vim
        /usr/share/vim/vim73/autoload/xml/xhtml10t.vim
        /usr/share/vim/vim73/autoload/xml/xhtml11.vim
        /usr/share/vim/vim73/autoload/xml/xsd.vim
        /usr/share/vim/vim73/autoload/xml/xsl.vim
        /usr/share/vim/vim73/autoload/xmlcomplete.vim
        /usr/share/vim/vim73/compiler/xmllint.vim
        /usr/share/vim/vim73/compiler/xmlwf.vim
        /usr/share/vim/vim73/ftplugin/xml.vim
        /usr/share/vim/vim73/indent/xml.vim
        /usr/share/vim/vim73/syntax/docbkxml.vim
        /usr/share/vim/vim73/syntax/xml.vim

There is nothing to google, nothing to install. It just works. 
Vim documentation is better resource than Google most times.

The trick is Vim's autoloading feature. You need to make sure the file you are
opening has the proper DOCTYPE definition which is correct. So use that for
HTML and XHTML files, then Vim 7+ will automatically enable XML/HTML omni
completion for you. Example for HTML4:

        <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
            "http://www.w3.org/TR/html4/loose.dtd">
        <html>
        </html>

Now try to insert body tag, type "bo" and hit Ctrl X O. Bang. Try to add an
attribute, type "on" and hit it again. Bingo.

You can use Ctrl X O and other features:

        - after "<" complete the tag name, depending on context
        - inside of a tag complete proper attributes
        - when an attribute has a limited number of possible values help to complete
          them
        - complete names of entities (defined in |xml-omni-datafile| and in the
          current file with "<!ENTITY" declarations)
        - when used after "</" CTRL-X CTRL-O will close the last opened tag

More info (and possible user customization with own XML definitioins) here:

http://vimdoc.sourceforge.net/htmldoc/insert.html#ft-xml-omni

