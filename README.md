# Bookworm and/or Redditworm?: a deep dive into Redditors' eloquency and education level

_Group members: Sebastian Weber, Cedric Krug, Kalypso Dimou_

## Introduction

Start off by setting the stage for your project. Give a brief overview of relevant studies or work that have tackled similar issues. Then, clearly describe the main question or problem your project is designed to solve.

## Dataset

The dataset used is Webis-TLDR-17 corpus which was yielded by a large Reddit crawl. The corpus consists of 3,848,330 preprocessed posts (submissions and comments from multiple subreddits in the time period 2006-2016). Each post is comprised of strings for 'author', 'body', 'normalizedBody', 'content', 'summary', 'subreddit' and 'subreddit_id' with the average word count being 270 words for 'content' and 28 words for 'summary'.

For the purposes of the current research, we mainly used the features of 'author', 'subreddit' and 'content'. To reduce the size of the data, we filtered out posts that .. and got rid of summaries completely.


## Methods

### Setup 


Outline the tools, software, and hardware environment, along with configurations used for conducting your experiments. Be sure to document the Python version and other dependencies clearly. Provide step-by-step instructions on how to recreate your environment, ensuring anyone can replicate your setup with ease:

```bash
conda create --name myenv python=<version>
conda activate myenv
```

Include a `requirements.txt` file in your project repository. This file should list all the Python libraries and their versions needed to run the project. Provide instructions on how to install these dependencies using pip, for example:

```bash
pip install -r requirements.txt
```

### Experiments

To calculate the education level of the Reddit users, the Gunning fog index was employed. 
The fog index is commonly used to confirm that text can be read easily by the intended audience. Texts for a wide audience generally need a fog index less than 12. Texts requiring near-universal understanding generally need an index less than 8.



For the preprocessing of the corpus, nine parameters were extracted in a csv file. The original features 'id', 'author', 'subreddit_id', 'subreddit' were maintained alongside the new data of 'word_count', 'syllable_count', 'complex_word_count' and 'readability_index'. The 'readablity' term may be a bit misleading, in light of its range being 6 to 17. The higher the number the more years of formal education  are needed to understand the text. 

Report how you conducted the experiments. We suggest including detailed explanations of the preprocessing steps and model training in your project. For the preprocessing, describe  data cleaning, normalization, or transformation steps you applied to prepare the dataset, along with the reasons for choosing these methods. In the section on model training, explain the methodologies and algorithms you used, detail the parameter settings and training protocols, and describe any measures taken to ensure the validity of the models.

## Results and Discussion

Present the findings from your experiments, supported by visual or statistical evidence. Discuss how these results address your main research question.

## Conclusion

Summarize the major outcomes of your project, reflect on the research findings, and clearly state the conclusions you've drawn from the study.

## Contributions

| Team Member    | Contributions                                             |
|----------------|-----------------------------------------------------------|
| Cedric Krug    | Data cleaning                                             |
| Sebastian Weber| Data transforming                                         |
|  Kalypso Dimou | Documentation                                             |

## References

Martin Potthast, Michael V{"o}lske, Benno Stein and Shahbaz Syed. 2017.  $${\color{lightblue}{TL};{DR}: Mining {R}eddit to Learn Automatic Summarization}$$ . In _Proceedings of the Workshop on New Frontiers in Summarization_, Association for Computational Linguistics, Copenhagen, Denmark, September 2017. pages 59-63. https://www.aclweb.org/anthology/W17-4508


