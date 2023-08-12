# climate-search-cli
A python program that can be run from the command line, and used to search climate policy documents.

## Task Overview

Created as an interview technical challenge. The task is to create a cli tool that can be used to search summaries of climate documents. 

The cli needed to have the following functionality:

- Load & validate documents into a database at the command line
- Query the documents returning a sequence of document objects
- Display the documents and some statistics about them as output
- Order by relevance using a relevancy score

## Evaluation Criteria

The following are the items that are being evaluated:

- Readability
- Maintainability
- Functionality
- Efficiency
- Modularity
- Commenting and documentation
- Testing Strategy


## Overview

Run poetry to install dependencies, (see below for other ways of running):
```
poetry install
poetry shell
```

Data can be loaded via:
```
cs load
```

This will also output errors to the same directory, and load the data into a database. A custom file can also be loaded using the --localpath argument. 

Data can then be queried by passing keywords with the retrieve command:

```
cs retrieve -k green -k energy
```

This will display the policies that match. Results can also be sorted with:

```
cs retrieve -k forests --sort
```


## Time taken

I worked intermittently on this over the course of a couple of days. I think the total time actively working on the solution was about 6 hours. (Not including time spent reading the brief, researching and planning). I could keep going, but I went over the suggested timeframe, so I'm leaving it here. Some key items I'd like to improve include error handling and the relevancy algorithm.

## alternate ways of running

### Docker

This can also be run via docker:

```
docker build -t climate-search-cli:latest .
```

```
docker run climate-search-cli:latest load
docker run climate-search-cli:latest retrieve -k cycling -k health --sort
```

### pypi

Also [available on pypi](https://pypi.org/project/climate-search-cli/):

```
pip install climate-search-cli
```
