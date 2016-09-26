import collections

InputWord = collections.namedtuple('InputWord', 'word type')
NextInfo = collections.namedtuple('NextInfo', 'word percent')

# Creates a hashmap to find what next words can follow. It's layed out as follows
# {
#     <starting_word>: {
#         <starting_word_type>: {
#             <next_word_type>: [
#                 (<next_word>, <transition_percent_chance>)
#             ],
#             ...
#         },
#         ...
#     },
#     ...
# }
def processInput(text):
    nexts = {}
    for line in text.split('\n'):
        parts = line.split('/')
        w1 = InputWord(parts[0], parts[1])
        w2 = InputWord(parts[3], parts[4])
        percent = float(parts[6])

        nexts.setdefault(w1.word, {})
        nexts[w1.word].setdefault(w1.type, {})
        nexts[w1.word][w1.type].setdefault(w2.type, [])
        nexts[w1.word][w1.type][w2.type].append(NextInfo(w2.word, percent))
    return nexts

Sentence = collections.namedtuple('Sentence', 'string percent')
Node = collections.namedtuple('Node', 'word depth sentence')

def generate(startingWord, sentenceSpec, graph):
    nexts = processInput(graph)

    bestSentence = None
    totalNodes = 0

    # we need to keep track of the depth of each node to look up which word type is next
    # we also need to keep track of the sentence generated so far and its percentage to print the answer
    nodes = [Node(startingWord, 1, Sentence(startingWord, 1.0))]

    # Function to generate next nodes given a node
    def generateNextNodes(node):
        nodes = []
        try:
            for next in nexts[node.word][sentenceSpec[node.depth-1]][sentenceSpec[node.depth]]:
                nodes.append(Node(
                    next.word,
                    node.depth+1,
                    # add the node's word to the sentence, multiplying the percents
                    Sentence(
                        node.sentence.string + " " + next.word,
                        node.sentence.percent*next.percent
                        )
                    ))
        except KeyError:
            # no need to do anything, nodes will be empty array
            pass
        return nodes

    while nodes != []:
        # take from the front for a breadth-first search
        node = nodes.pop(0)
        totalNodes += 1
        if node.depth < len(sentenceSpec):
            nodes.extend(generateNextNodes(node))
        elif bestSentence is None or node.sentence.percent > bestSentence.percent:
            bestSentence = node.sentence
    return("\"" + bestSentence.string + "\" with probability " + str(bestSentence.percent) + \
            "\nTotal nodes considered: " + str(totalNodes))


def main():
    text = open("input.txt").read()
    print generate("hans", ["NNP", "VBD", "DT", "NN"], text)

if __name__ == "__main__":
    main()
