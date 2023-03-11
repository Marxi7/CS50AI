import csv
import itertools
import sys
import numpy as np

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)

    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # Initializing the joint probability to 1 -> will change during the iterations
    joint_probability = 1

    # For each  person in a family
    for person in people:

        gene_copies = 1 if person in one_gene else 2 if person in two_genes else 0

        has_trait = False if person not in have_trait else True

        person_trait_probability = PROBS['trait'][gene_copies][has_trait]

        mother = people[person]['mother']
        father = people[person]['father']

        # If person has no parents -> basic probability based on the Probs dict.
        if mother is None or father is None:
            person_gene_probability = PROBS['gene'][gene_copies]

        # If person has parents -> probability based on the probability of parents giving gene
        else:
            mother_gene_probality = probability_from_parent(mother, one_gene, two_genes)
            father_gene_probality = probability_from_parent(father, one_gene, two_genes)

            if gene_copies == 0:
                # Probability of each parent not having the gene
                person_gene_probability = (1 - mother_gene_probality) * (1 - father_gene_probality)
            
            elif gene_copies == 1:
                # Chance of child having gene from mother but not father and vice versa
                chance_from_mother_not_father = mother_gene_probality * (1 - father_gene_probality)
                chance_from_father_not_mother = father_gene_probality * (1 - mother_gene_probality)

                # Probability of child having gene from parents
                person_gene_probability = chance_from_mother_not_father + chance_from_father_not_mother
            
            else:
                # Probability of each parent having the gene
                person_gene_probability = mother_gene_probality * father_gene_probality
        
        chance_HasGeneAndtraitDisplay = person_gene_probability * person_trait_probability

        # For each iteration in people, we update the joint probability by multiplying 
        # it with the current person's chance of having the gene and a trait.
        joint_probability *= chance_HasGeneAndtraitDisplay
    
    return joint_probability


def probability_from_parent(parent, one_gene, two_genes):
    """
    This function computes the probability that a parent give the gene to the child 
    depending on the number of gene copies that parent has
    1. If a parent has one copy of the mutated gene, then the probability of passin the gene is 0.5
    2. If a parent has two copies of the mutated gene, then the probability of passin the gene is 1 - possible mutation
    3. If a parent has 0 copies of the mutated gene, then the probability of passin the gene is the possible mutation
    """
    if parent in one_gene:
        return 0.5
    elif parent in two_genes:
        return 1 - PROBS["mutation"]
    else:
        return PROBS['mutation']

            
def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:

        gene_copies = 1 if person in one_gene else 2 if person in two_genes else 0
        has_trait = False if person not in have_trait else True

        # Updating each person's "gene" and "trait" distributions
        probabilities[person]['gene'][gene_copies] += p
        probabilities[person]['trait'][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:

        probability_gene_values = probabilities[person]['gene'].values()
        probability_trait_values = probabilities[person]['trait'].values()

        # Normalizing the gene and trait distributions
        # inspired from this : https://stackoverflow.com/questions/26785354/normalizing-a-list-of-numbers-in-python
        probabilities[person]['gene'] = {gene: (its_probability / sum(probability_gene_values)) 
                                         for gene, its_probability in probabilities[person]['gene'].items()}

        probabilities[person]['trait'] = {trait: (its_probability / sum(probability_trait_values))                                       
                                          for trait, its_probability in probabilities[person]['trait'].items()}
    

if __name__ == "__main__":
    main()