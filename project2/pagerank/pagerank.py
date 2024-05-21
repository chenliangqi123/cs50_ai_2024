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
    distribution = {}
    total_pages = len(corpus)
    out_links = corpus[page]

    if not out_links:
        for p in corpus:
            distribution[p] = 1 / total_pages
    else:
        for p in corpus:
            distribution[p] = (1 - damping_factor) / total_pages
        for link in out_links:
            distribution[link] += damping_factor / len(out_links)

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        page_ranks[current_page] += 1
        probabilities = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]

    total = sum(page_ranks.values())
    for page in page_ranks:
        page_ranks[page] /= total

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    page_ranks = {page: 1 / num_pages for page in corpus}

    # Loop until convergence
    threshold = 0.001
    change = float('inf')

    while change > threshold:
        new_ranks = {}
        change = 0

        for page in corpus:
            rank_sum = 0
            for potential_linker in corpus:
                if page in corpus[potential_linker]:
                    rank_sum += page_ranks[potential_linker] / len(corpus[potential_linker])
                if not corpus[potential_linker]:  # Handle dead-end page
                    rank_sum += page_ranks[potential_linker] / num_pages

            new_rank = (1 - damping_factor) / num_pages + damping_factor * rank_sum
            new_ranks[page] = new_rank
            change += abs(page_ranks[page] - new_rank)

        page_ranks = new_ranks

    return page_ranks


if __name__ == "__main__":
    main()
