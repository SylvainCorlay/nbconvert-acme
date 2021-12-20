# nbconvert-flowkey

Python package for custom `nbconvert` template used when exporting Jupyter notebooks to HTML reports. The source code here can be packaged into a PyPI wheel with data files, using the logic provided from the original repo from which this was forked (see [License](##license)).
This repo also includes a [sample notebook](notebooks/demo.ipynb) for demo purposes.

## Installation

:warning: This has been only tested on macOS 11.5.2 (with Miniconda3 installation) and within a Docker container built off `python:3.9-slim` (Linux; Debian). 

To try it out, I would recommend installing the package via the provided [Docker Image](Dockerfile), and running the demo as follows:

```bash
#build the image
docker build -t nbconvert-demo .

#run the demo
docker run -it --rm -v $PWD:/usr/src/myapp nbconvert-demo
```

Then open up the generated report!

```bash
open notebooks/report.html
```

## Usage

Once installed (even outside Docker), the custom template will be available to you when convert a notebook to HTML:

```bash
jupyter nbconvert notebooks/demo.ipynb --to html --no-input --output 'report.html' --template flowkey
```

## How it Works

What has happened underneath the hood to make this custom template available to you is that the [data files](share/jupyter/nbconvert/templates/flowkey) in this repo
have been installed locally (or within Docker) at the following location:

```
<sys.prefix>/share/jupyter/nbconvert/templates/flowkey
```

, where [sys.prefix](https://docs.python.org/3/library/sys.html#sys.prefix) specifies the directory prefix where platform-independent
Python files are installed; by default, this is the string `/usr/local`. All this logic is specified in the [setup.py](setup.py) file -- 
thanks to [Sylvain Corlay](https://github.com/SylvainCorlay/nbconvert-acme) for doing most of the heavy lifting!

## Limitations / Future Improvements

What I would love to do is incorporate a smarter / more dynamic table of contents (TOC) feature into the 
HTML export. The [toc2 juptyer extension](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/toc2/README.html)
is very nice, but unfortunately doesn't work with `nbconvert > 6`. Attempts at building my own custom nbconvert
exporter were not successful, and the efforts to make this HTML template backwards compatible with `nbconvert==5.6.1` are not worth the trouble.

Therefore, for the time being, I built a simple, manual "nax box" button that simply hyperlinks the user back to the 
table of contents at the top of page. The only catch is that in order for it to work, you must create a markdown
header with an id of "`contents`", e.g.:

```markdown
## Contents<a class="anchor" id="contents"></a>:
```


## License

As hinted earlier, this repository was heavily adapted from the original source code by [Sylvain Corlay](https://github.com/SylvainCorlay),
and originally found from the [Jupyter Blog](https://blog.jupyter.org/the-templating-system-of-nbconvert-6-47ea781eacd2)
written by the same author.

As such, this software is published under the conditions of the original license:

*We use a shared copyright model that enables all contributors to maintain the
copyright on their contributions.*

*This software is licensed under the BSD-3-Clause license. See the
[LICENSE](LICENSE) file for details.*
