#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='furigana', 
	version='0.1',
	description='''convert Kanji in Japanese into Kanji with Hiragana placed above (Furigana(振り仮名)). For example, "澱んだ街角" => "澱(よど)んだ街角(まちかど)" ''',
	author='Miki.Liu',
	author_email='mikimotoh@gmail.com',
	url='https://github.com/MikimotoH/furigana',
	packages=['furigana'],
	classifiers=[
	    # How mature is this project? Common values are
	    #   3 - Alpha
	    #   4 - Beta
	    #   5 - Production/Stable
	    'Development Status :: 3 - Alpha',

	    # Indicate who your project is intended for
	    'Intended Audience :: Developers',
	    'Topic :: Software Development :: Build Tools',

	    # Pick your license as you wish (should match "license" above)
	    'License :: OSI Approved :: MIT License',

	    # Specify the Python versions you support here. In particular, ensure
	    # that you indicate whether you support Python 2, Python 3 or both.
	    'Programming Language :: Python :: 3',
	    'Programming Language :: Python :: 3.2',
	    'Programming Language :: Python :: 3.3',
	    'Programming Language :: Python :: 3.4',
	    ],
	keywords='Japanese Language Processing',
	)
