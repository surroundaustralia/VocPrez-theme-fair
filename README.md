# VocPrez FAIR Score theme
A VocPrez UI theme for demonstrating a FAIR score calculator.

This repository contains stylistic and content elements that are overlaid onto an instance of [VocPrez](https://github.com/RDFlib/VocPrez), the Python SKOS Vocabulary publication tool, to enable demonstration scores of [FAIR Principles](https://ardc.edu.au/resources/working-with-data/fair-data/). Items delivered by VocPrez - vocabularies - then have a new _profile_ or _view_ of them that communicates a FAIR score made up of values for F, A, I & R as well as an indication of the method that was used to genetate the scores.

## Use
`apply.sh` adds these elements - templates, style files and extra API endpoints - to a VocPrez instance

The only config needed is to set the following environment variables before using `apply.sh`:

* `$VP_THEME_HOME` - installation dir of this theme, no trailing slash
* `$VP_HOME` - installation dir of VocPrez, no trailing slash

## Contact
*publisher:*  
![](SURROUND-logo-100.png)  
**SURROUND Australia Pty. Ltd.**  
<https://surroundaustralia.com>  

*creator:*  
**Dr Nicholas J. Car**  
*Data Systems Architect*  
SURROUND Australia Pty. Ltd.  
<nicholas.car@surroudaustralia.com>  
![](orcid.png) [0000-0002-8742-7730](https://orcid.org/0000-0002-8742-7730)