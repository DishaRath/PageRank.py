
import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}:{ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a dictinary of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only in links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability 'damping_factor', choose a link at random
    linked to by 'page'. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    d = {}
    links = corpus[page]
    num_pages = len(corpus)
    num_links = len(links)

    if (links):
        # assigns prob (1 - damping_factor)/ num_pages to each key of the corpus
        for key in corpus:
            d[key] = (1 - damping_factor) / num_pages
 
        # assigns probs damping_factor / num_links for each key (page) in corpus.
        for key in links:
            d[key] += damping_factor / num_links

    else:
        # if a page has no links from it, assigns prob of 1 / num_pages
        for key in corpus:
            d[key] = 1.0 / num_pages

    return d


def sample_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value ( a value between 0 and 1). All
    PageRank values should sum to 1
    """
    d = {}.fromkeys(corpus.keys(), 0)
    page = random.choices(list(corpus.keys()))[0]

    for i in range(1, n):
        current_dist = transition_model(corpus, page, damping_factor)
        for _page in d:
            d[_page] = (((i - 1) * d[_page]) + current_dist[_page]) / i
        page = random.choices(list(d.keys()), weights=list(d.values()), k=1)[0]

    return d


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    distribution = {}.fromkeys(corpus.keys(), 1.0 / total_pages)
    change = True

    while change:
        change = False
        old_distribution = copy.deepcopy(distribution)
        for page in corpus:
            distribution[page] = ((1 - damping_factor)/total_pages) + \
                (damping_factor * get_sum(corpus, distribution, page))
            change = change or abs(
                old_distribution[page] - distribution[page]) > 0.001

    return distribution


def get_sum(corpus, distribution, page):
    result = 0
    for p in corpus:
        if page in corpus[p]:
            result += distribution[p] / len(corpus[p])
    return result


if _name_ == "_main_":
    main()

        
    
        
            
        
    
    
    
