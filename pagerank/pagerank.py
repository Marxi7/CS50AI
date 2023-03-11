import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
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

    # Only include links to other pages in the corpus
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

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {}

    number_of_links_current_page = len(corpus[page])
    number_of_pages_in_corpus = len(corpus)

    if number_of_links_current_page != 0:
        # Probability per page -> (1 - d) / N
        for link in corpus:
            probability_distribution[link] = (1 - damping_factor) / number_of_pages_in_corpus
        
        # Probability per link in current page
        for link in corpus[page]:
            probability_distribution[link] += damping_factor / number_of_links_current_page
    else:
        # Return a probability distribution that chooses randomly among all pages with equal probability
        for link in corpus:
            probability_distribution[link] = 1 / number_of_pages_in_corpus
    
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageRank = {}
    # Initializing the dictionary
    pageRank = {page: 0 for page in corpus}

    pages_in_corpus = list(corpus.keys())

    # First sample page -> random page in corpus
    page = random.choice(pages_in_corpus)

    for i in range(1, n):
        current_probability_distribution = transition_model(corpus, page, damping_factor)
        
        # Update the PageRank scores of each page
        for page in pageRank:
            pageRank[page] = (current_probability_distribution[page] + (i - 1) * pageRank[page]) / i

        page_rank_keys = list(pageRank.keys())
        page_rank_values = list(pageRank.values())

        # Select a new random page based on its PageRank score 
        # -> https://www.w3schools.com/python/ref_random_choices.asp
        page = random.choices(page_rank_keys, page_rank_values, k=1)[0]

    return pageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    number_of_pages_in_corpus = len(corpus)
    pageRank = {}

    # Initialize PageRank values
    pageRank = {page: 1 / number_of_pages_in_corpus for page in corpus}

    while True:
        new_pageranks = {page: (1 - damping_factor) / number_of_pages_in_corpus for page in corpus}
        
        # Updating the pageRanks
        for page in corpus:
            for linked_page in corpus[page]:
                new_pageranks[linked_page] += (damping_factor * pageRank[page]) / len(corpus[page])
        
        diff = max([abs(pageRank[page] - new_pageranks[page]) for page in corpus])
        if diff < 0.001:
            break
        
        pageRank = new_pageranks
        
    # For each page in the pageRank dictionary, a key-value pair is added to the dictionary normalized_pageranks, 
    # where the key is the page and the value is the page's rank in the pageRank dictionary divided by the sum of all the ranks in the pageRank dictionary. 
    # This normalizes the ranks so that they sum up to 1.
    normalized_final_pageRanks = {page: pageRank[page] / sum(pageRank.values()) for page in pageRank}

    return normalized_final_pageRanks


if __name__ == "__main__":
    main()