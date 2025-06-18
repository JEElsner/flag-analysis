# Fun with Flags! (flag-analysis)

Flags are an important symbol of a nation, putting its values and heritage on display for the world. As such, it is important that a flag be well designed and distinctive. We use data analysis to examine similarities and differences between national flags to identify patterns in flag design.

In this project, we scrape descriptions of national flags from Wikipedia, mine the text for key features, fit clustering models to identify similar flags, and plot the pretty results.

## Development

*Caveat Emptor: Since Wikipedia can be edited and modified at any time, the data scraping may not work as originally created. Also, be kind and don't scrape Wikipedia too much.*

There are three main files in this project: `load_data.ipynb`, which attempts to scape text descriptions of the flags from Wikipedia as well as download thumbnails of each flag; `text_mining.ipynb`, which mines the downloaded text; and `data_analysis.ipynb`, which fits the clustering models, and creates the plots. Run the notebooks in the order above to *theoretically* reproduce the results.

### Installation

This project uses [pdm](https://pdm-project.org) to manage the project, the environment and Python modules. After [installing](https://pdm-project.org/en/latest/#installation) it, run the following command:

```bash
pdm install
```

This creates a virtual environment and installs the necessary packages. Done!

### Compilation of Writeup
With a suitable installation of LaTeX, run the following command:
```bash
latexmk --pdf 'Fun with Flags.tex'
```
