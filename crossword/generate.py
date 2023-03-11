import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # For each domain
        for domain in self.domains.keys():
            words_to_remove = set()

            for word in self.domains[domain]:
                if len(word) != domain.length:
                    words_to_remove.add(word)
            # Updating the domain if there is any word to remove
            self.domains[domain] -= words_to_remove

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        words_to_remove = set()
        overlap_x_y = self.crossword.overlaps[x, y]

        if overlap_x_y is None:
            return False

        i, j = overlap_x_y
        for first_word in self.domains[x]:
            for second_word in self.domains[y]:
                if first_word[i] == second_word[j]:
                    break
            else:
                # if ith and jth letters are not the same, we'll remove the word (value)
                # from the variable (domain) x in order to make it consistent with the variable (domain) Y
                words_to_remove.add(first_word)
                revised = True
        
        # Updating the variable x by removing the words or which there is no possible corresponding value for `y`
        if words_to_remove:
            self.domains[x] -= words_to_remove

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is not None:
            queue = [arc for arc in arcs]

        else:
            queue = []
            for x in self.domains.keys():
                for y in self.domains.keys():
                    if x != y:
                        queue.append((x, y))
        
        while queue:
            (X, Y) = self.Dequeue(queue)

            if (X, Y) is not None:
                if self.revise(X, Y):
                    if len(self.domains[X]) == 0:
                        return False
                    
                    for Z in self.crossword.neighbors(X):
                        queue.append((Z, X))
        return True

    def Dequeue(self, queue):
        """
        This function remove x, y from the queue and return x, y so we can revise it in our ac3 function
        """
        for x, y in queue:
            queue.remove((x, y))
            return (x, y)

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for domain in self.domains:
            if domain not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Kepping track of the used keys
        already_used_keys = []

        for key, word in assignment.items():
            if key.length != len(word):
                return False

            # Making sure a key isn't used twice
            if key not in already_used_keys:
                already_used_keys.append(key)
            else:
                return False
            
            # Getting all the neighbors
            neighbors = self.crossword.neighbors(key)

            for neighbor_key in neighbors:
                # Getting the overlapping value between word1 and word2
                overlap = self.crossword.overlaps[key, neighbor_key]
                key_overlap = overlap[0]
                neighbor_key_overlap = overlap[1]

                if neighbor_key in assignment:
                    word2 = assignment[neighbor_key]
                    # If ith letter of word 1 doesn't match jth letter of word 2 - based on the overlap
                    if word[key_overlap] != word2[neighbor_key_overlap]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        word_count = {}

        neighbors = self.crossword.neighbors(var)
        words = self.domains[var]

        for word in words:
            word_count[word] = 0
            if word not in assignment:
                for neighbor in neighbors:
                    if word in self.domains[neighbor]:
                        word_count[word] += 1
        # Sorting the keys by the value in an ascendind order -> returning a sorted list
        sorted_list = sorted(word_count, key=lambda key: word_count[key])

        return sorted_list
 
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        all_domains = set(self.domains.keys())
        domains_in_assignment = set(assignment.keys())

        unassigned_variables = list(all_domains - domains_in_assignment)
        domain_nb_values = {}
        
        for variable in unassigned_variables:
            domain_nb_values[variable] = 0
            if len(self.domains[variable]) > 0:
                domain_nb_values[variable] = len(self.domains[variable])
        
        return min(unassigned_variables, key=lambda key: (domain_nb_values[key], len(self.crossword.neighbors(key))))
        
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if len(assignment.keys()) == len(self.domains.keys()):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            # Removing var from assigment
            assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()