# About this book

This book is a collection of course notes adapted from ...

## Copyright

Creative commons for my intellectual property.  EPANET itself is public domain.  Some content is taken from OWS [http://wateranalytics.org/](http://wateranalytics.org/) and use of that material is covered by their copyright.  As far as I know, all content is either public domain or shareable with attribution.  

## Suggested Citation

Cleveland, T.G. 2023. Hydraulic Network Simulation with EPANET and Python.  Notes to accompany Metropolia ICT Summer School 2023 Course TX00FJ07 DOI...

:::{note}
I intend to build this entire book into a PDF file; at that time I can get a DOI and will edit the above listing.  This document is intended to be a living on-line book, and not a static PDF - but a static PDF is only way I can easily create a permanent DOI.  Until that time, content will grow as parts are added/updated
:::

## Git-Hub Repository

This book and supporting files are located in a public repository on GitHub at [https://github.com/dustykat/ects-epanet/blob/main/README.md](https://github.com/dustykat/ects-epanet/blob/main/README.md).  To recreate the book, clone the repository into your /var/www/html directory (or whatever your webroot is). Then create an entry point to `http://YOUR-WEBROOT/ects-epanet/ects-epanet-notes/_build/html/index.html` and you should have the book. If you clone the book, you should also get the shared object (.so) library built for my Raspberry Pi.  I am not sure it entirely works this way - I left notes to build your own in the book.  Windows folks have much better support as the .dll distribute from the EPA website, and I dont think you have to build your own modules.

:::{note}
Some of the links herein are to a specific TCP/IP address and you will need to change it to your webroot for the links to work.  If you went to the trouble to clone and rebuild, the prefix (IP address) is obvious; if the address also contains "ects-epanet" then you have the file in the repository and changing the prefix to your webroot will restore the link.

Links with the prefix `http://54.243.252.9` are on a different server, that does not have a DNS entry.  If you wish to to have a complete copy of the notebook webroot, you will have to take these links to the resource, copy it to your host and adjust the link URL - this was not intentional, just a consequence of learning as I go in how to build web resources.
:::

The `freeswmm.ddns.net` is a little more complicated.  It is a Linux instance running on AWS servers, there are ways to transfer and copy instances, but you are probably better served to just buy a suitable computer if you need to use it for serious computation.


