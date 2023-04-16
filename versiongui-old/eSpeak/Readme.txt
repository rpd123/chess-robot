eSpeak is a compact, multi-language, open source
text-to-speech synthesizer.

This version is a SAPI5 compatible Windows speech engine
which should work with screen readers such as Jaws,
NVDA, and Window-Eyes.

There is also a version of eSpeak which can be run as a
command-line program.  This is in eSpeak\command-line.
Read docs\commands.html for details.

License
=======

This software is licensed under the GNU General Public License
version3.  See the file:  License.txt.


Voices and Languages
====================

The available Voices can be seen as files in the directory
  espeak-edit/voices.

To change which eSpeak Voices are available through
Windows, re-run the installer and specify the Voice files
which you want to use.

The tone of a Voice can be modified by adding a variant
name after the Voice name, eg:
  pt+f3

The available variants are:
Male:    +m1  +m2  +m3  +m4  +m5  +m6  +m7
Female:  +f1  +f2  +f3  +f4  +f5
Other effects:  +croak  +whisper
A different synthesizer method: klatt  klatt2  klatt3

These variants are defined by text files in
  espeak-edit/voices/!v


TTSApp Application
==================

This is a test program provided by Microsoft which can be
used to speak text using SAPI5 voices.  The eSpeak voices
which were specified during installation should appear in
its voice menu.

Select its "22050Hz 16-bit mono" option for speaking.


Updates
=======

The eSpeak project homepage is at:
  http://espeak.sourceforge.net/

Comments, corrections, and other feedback and assistance
is sought from native speakers of the various languages
because I've no idea how they are supposed to sound :-)

To make changes to pronunciation rules and exceptions,
or to change the sounds of phonemes, or just to experiment
with speech synthesis, download the "espeakedit" program.


