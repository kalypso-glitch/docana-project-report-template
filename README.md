
# Bookworm and/or Redditworm?: a Deep Dive into Redditors' Eloquency and Education Level

_Group members: Sebastian Weber, Cedric Krug, Kalypso Dimou_

## Introduction

The social media platform of Reddit is a place for people to ask questions, find community and exchange advise+

to be revised:
(Moore & Chuang, 2017) 
"Reddit is categorized as a social news site by Alexa and is the second most trafficked news-related site, ranking above CNN and Fox News. It is the highest
ranked news aggregator site by a wide margin, according to Alexa’s rankings. Reddit users, known as Redditors, have played and
are playing a vital role in this new way people interact online. Web 2.0 platforms and sites like Reddit are also changing how news content is disseminated and
shared as the relationship between people and media is evolving.
Reddit is more than a place to post news content; it has evolved into a massive, thriving, highly influential virtual community. With its ever-growing cadre
of Subreddits, specialized areas focusing on a wide variety of topics, Reddit is more like a metacommunity. In a meta-community discrete
communities—individual and grouped Subreddits— are linked by the diffusion of interacting species— individual users and groups of users who subscribe to
many Subreddits and interact across them. Reddit has been referred to as both a culture and many cultures because of the complex interactions across Subreddits. Users, employing sometimes one, sometimes many Reddit usernames, move seamlessly from Subreddit to Subreddit and spread content across Subreddits on the site, which are interwoven to create Reddit as a recognizable entity outside of the Reddit user community as a whole."
"(number one factor for posting on Reddit) Socializing/community building as a factor in posting content is consistent with the literature, explained by the concept of anticipatory socialization. Anticipatory socialization means that users obtain social gratifications from sharing original or curated content with other users. Aggregators, like Reddit, are virtual communities where sharing content facilitates social connections "
"They also reinforce existing social connections through posting comments that agree or disagree with comments by other users. Users also help to enforce
community standards through commenting (calling out trolls or those who are reposting content from another user and claiming it as original); thereby,
strengthening the community of individual Subreddits and Reddit as a meta-community. Self-policing when it comes to agreed-upon behaviors is a crucial part of building and maintaining communities, both in person and online."

(Mucan & Özgüven, 2022)
"Social media websites are designed to be widely accessible and initially attract homogeneous populations, so it is not uncommon
to find groups using websites to segregate themselves according to nationality, age, educational level, or other factors that typically segment society, even if that was not the intention of the designers (Boyd & Ellison, 2008) Boyd, D., & Ellison, N. (2008). Social network sites: Definition, history, and scholarship. Journal of Computer-Mediated Communication, 13, 210-230. http://doi.org/gzn"
"it was found that as levels of education and income increase social media use also increases." also backed by (Hruška & Maresova, 2020)

## Dataset

The dataset used is Webis-TLDR-17 corpus which was yielded by a large Reddit crawl. The corpus consists of 3,848,330 preprocessed posts (submissions and comments from multiple subreddits in the time period 2006-2016). Each post is comprised of strings for 'author', 'body', 'normalizedBody', 'content', 'summary', 'subreddit' and 'subreddit_id' with the average word count being 270 words for 'content' and 28 words for 'summary'.

For the purposes of the current research, we mainly used the features of 'author', 'subreddit' and 'content'. To reduce the size of the data, we filtered out posts with less than 100 words (_right?_) and got rid of summaries completely.


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

To calculate the education level of the Reddit users, the Gunning fog index was employed, which is calculated by the formula:

<img width="500" height="77" alt="{B7350756-3256-43AF-A810-0D6B69B0173E}" src="https://github.com/user-attachments/assets/45bdc065-08da-4b2a-8c92-1f9a86c777c2" /> 


First we needed to find the average number of sentences, words and complex words in each post and so, nine parameters were extracted in a csv file. The original features 'id', 'author', 'subreddit_id', 'subreddit' were maintained alongside the new data of 'word_count', 'syllable_count', 'complex_word_count' and 'readability_index'. The 'readablity' term may be a bit misleading, in light of its range being 6 to 17. The higher the number the more years of formal education  are needed to understand the text. The fog index is commonly used to confirm that an intended audience can easily read a text. Texts targeted to a wide audience generally need a fog index less than 12, or less than 8 for a near-universal understanding (DuBay, 2004).

For the cleaning of the data, non Latin alphabet characters were ignored, as well numeric values, using the regular expression (r'\w+').


## Results and Discussion

Present the findings from your experiments, supported by visual or statistical evidence. Discuss how these results address your main research question.

## Conclusion

Summarize the major outcomes of your project, reflect on the research findings, and clearly state the conclusions you've drawn from the study.

## Contributions

| Team Member    | Contributions                                             |
|----------------|-----------------------------------------------------------|
| Cedric Krug    | Data cleaning     ...                                     |
| Sebastian Weber| Data transforming   ...                                   |
| Kalypso Dimou  | Documentation     ...                                     |

## References
Carrie Moore and Lisa Chuang. 2017. $${\color{blue}Redditors \space Revealed:\space Motivational\space Factors\space of\space the\space Reddit\space Community}$$. 10.24251/HICSS.2017.279. 

Jan Hruška and Petra Maresova. 2020. $${\color{blue}Use of Social Media Platforms among Adults in the United States—Behavior on Social Media}$$. Societies. _10_. 10.3390/soc10010027. 

Martin Potthast, Michael V{"o}lske, Benno Stein and Shahbaz Syed. 2017.  $${\color{blue}{TL};{DR}: Mining {R}eddit to Learn Automatic Summarization}$$ . In _Proceedings of the Workshop on New Frontiers in Summarization_, Association for Computational Linguistics, Copenhagen, Denmark, September 2017. pages 59-63. https://www.aclweb.org/anthology/W17-4508

Burcu Mucan and Nihan Özgüven. 2013. $${\color{blue}The Relationship Between Personality Traits and Social Media Use}$$. Social Behavior and Personality, _41(3)_, pages 517-528. http://dx.doi.org/10.2224/sbp.2013.41.3.517.

William H. DuBay. 2004. $${\color{blue}Judges Scold Lawyers for Bad Writing}$$. Plain Language at Work Newsletter _(8)_. Impact Information. Archived from the original on 24 December 2013.

The Gunning's Fog Index (or FOG) Readability Formula. Readability Formulas.
