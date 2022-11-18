import spacy
from string import punctuation
from heapq import nlargest
import re

global stop_words
stop_words=['eleven', 'with', 'into', 'same', 'noone', 'per', '’ll', 'those', '’m', 'nothing', 'wherever', 'elsewhere', 'there', 'never', 'four', 'call',
                'each', 'can', 're', 'must', 'afterwards', 'myself', 'front', 'mine', 'until', 'ourselves', 'then', 'hereby', 'whence', 'thereupon', "'ve", 'whatever', 'but',
                'whose', 'is', 'alone', 'she', 'sixty', 'too', 'somewhere', 'everywhere', 'again', 'therefore', 'an', 'just', 'move', 'not', '’re', 'were', '‘re', 'always', 'her',
                'during', 'they', 'top', 'behind', 'please', 'along', 'give', 'themselves', 'say', 'one', '‘m', 'five', 'did', 'against', 'meanwhile', 'yours', 'whether', 'everyone',
                'does', 'towards', 'could', '’d', 'forty', 'of', 'over', 'some', 'was', 'n‘t', 'seemed', 'any', 'ever', 'have', 'used', 'almost', "'re", 'whom', '‘d', 'only', 'through',
                'itself', 'out', 'thereby', 'or', 'very', 'toward', 'n’t', 'between', 'him', '‘s', 'them', 'fifteen', 'and', 'via', 'part', 'full', 'might', 'below', 'nowhere', 'off',
                'throughout', 'down', 'than', 'once', 'many', 'your', 'himself', 'because', 'for', 'such', 'beyond', 'thru', 'anyway', 'across', 'these', 'further', 'sometime', 'which',
                "'s", 'various', 'under', 'about', 'less', 'take', 'onto', 'here', 'seeming', 'third', 'as', 'else', 'should', 'us', 'nobody', 'my', 'are', 'he', 'this', 'becomes', 'name',
                'it', 'empty', 'had', 'former', 'when', 'whole', 'become', 'since', 'therein', 'every', 'without', '’ve', 'anyhow', 'another', 'be', 'side', 'me', 'ten', 'amount', 'hers',
                'its', 'after', 'whereafter', 'above', 'in', 'whoever', 'among', 'put', 'whither', 'been', 'though', 'other', 'fifty', 'also', 'upon', 'two', 'hereafter', 'regarding', 'get',
                'sometimes', 'done', 'before', 'whereby', 'his', 'we', 'somehow', 'see', 'enough', 'perhaps', 'nevertheless', 'yourselves', 'no', 'what', 'around', 'together', 'others', 'within',
                'to', 'really', 'indeed', 'both', 'make', 'first', 'seem', 'where', 'six', 'using', 'made', 'all', 'has', 'hence', 'often', 'anywhere', "'m", 'several', 'quite', 'by', 'none',
                'last', 'still', 'latter', 'being', 'herein', 'rather', 'already', 'yet', 'that', 'serious', 'who', 'thus', 'the', 'go', 'unless', 'nine', 'so', 'i', 'due', 'much', 'nor',
                'twenty', 'whereas', 'twelve', 'moreover', 'their', 'more', 'least', 'either', 'will', 'latterly', 'ca', 'own', 'although', '’s', 'back', 'anything', 'a', 'namely', 'next',
                'doing', 'well', "'ll", 'ours', 'seems', 'besides', 'hereupon', 'cannot','herself', 'up', 'am', '‘ll', 'except', 'someone', 'formerly', 'our', 'amongst', 'neither', 'becoming',
                'on', 'show', 'something', 'if', 'yourself', 'everything', 'few', '‘ve', 'keep', 'whereupon', 'at', 'however', 'otherwise', 'beside','why', "n't", 'even', 'beforehand', 'mostly',
                'do', 'most', 'how', 'now', 'wherein', 'may', 'from', 'would', 'eight', "'d", 'whenever', 'became', 'thence', 'while', 'bottom', 'hundred', 'you', 'three', 'anyone', 'thereafter']


def summarize(text):
    #create natural language model
    NLP=spacy.load("en_core_web_sm")

    #pass text through our model
    article=NLP(text)

    #word frequency
    word_frequency=get_word_frequency(article,stop_words)
    
    #Normalise word frequency
    max_frequency=max(word_frequency.values())

    for word in word_frequency.keys():
        word_frequency[word]=word_frequency[word]/max_frequency

    #Sentence tokenisation
    sentence_tokens=[sent for sent in article.sents]

    #Sentence score
    sentence_score=get_sentence_score(sentence_tokens,word_frequency)

    #Summary
    select_length=int(len(sentence_tokens)*0.3)

    summary_list=nlargest(select_length,sentence_score,key=sentence_score.get)
    final_summary=[word.text for word in summary_list]
    summary=" ".join(final_summary)

    # Regext pattern to match all newline characters
    pattern = "[\n|\r|\n\r]"
    # Delete all newline characters from string
    summary = re.sub(pattern, '', summary )
    return summary

def get_word_frequency(article,stop_words):
    #Word frequency

    word_frequency={}
    for word in article:
        if word.text.lower() not in stop_words:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequency.keys():
                    word_frequency[word.text]=1
                else:
                    word_frequency[word.text]+=1
    return word_frequency


def get_sentence_score(sentence_tokens,word_frequency):
    sentence_score={}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequency.keys():
                if len(sent.text.split(' '))<30:
                    get_score(sent,word,sentence_score,word_frequency)
    return sentence_score

def get_score(sent,word,sentence_score,word_frequency):
    if sent not in sentence_score.keys():
        sentence_score[sent]=word_frequency[word.text.lower()]
    else:
        sentence_score[sent]+=word_frequency[word.text.lower()]
    return sentence_score