# svg-cleaner

Small Python tool which converts an SVG file into its most barebones version, for use within HTML code:
* Removes useless information from SVG editors such as Inkscape or Illustrator.
* Removes invisible layers and paths.
* In Angular mode, removes flow* tags.

## Usage

```shell
python3 ./svg_cleaner.py (-a | --angular) [SVG_FILE]
```

### Options

#### `-h, --help`
Prints the help message

#### `-a, --angular`
Enables Angular mode

## TODO

* Print to standard output to be more POSIX-like.
