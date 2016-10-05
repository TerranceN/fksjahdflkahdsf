import collections
from heapq import *

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
        if line != "":
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
Node = collections.namedtuple('Node', 'word depth sentence weighting')

def generate(startingWord, sentenceSpec, strategy, graph):
    strategy = strategy.lower()
    if not strategy in ['breadth_first', 'depth_first', 'heuristic']:
        return('invalid strategy')

    nexts = processInput(graph)

    bestSentence = None
    totalNodes = 0

    # we need to keep track of the depth of each node to look up which word type is next
    # we also need to keep track of the sentence generated so far and its percentage to print the answer
    nodes = [Node(startingWord, 1, Sentence(startingWord, 1.0), 1.0)]

    def heuristic_value(base, node):
        return base ** node.depth

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
                        node.sentence.string + ' ' + next.word,
                        node.sentence.percent*next.percent
                    ),
                    node.sentence.percent*next.percent * heuristic_value(0.1, node)))
        except KeyError:
            # no need to do anything, nodes will be empty array
            pass
        return nodes

    while nodes != []:
        node = None
        if strategy == 'breadth_first':
            # take from the front for a breadth-first search
            node = nodes.pop(0)
        elif strategy == 'depth_first':
            node = nodes.pop(len(nodes)-1)
        elif strategy == 'heuristic':
            node = nodes.pop(0)
        totalNodes += 1
        if node.depth < len(sentenceSpec):
            nextNodes = generateNextNodes(node)
            if strategy == 'heuristic':
                for nextNode in nextNodes:
                    heappush(nodes, nextNode)
            else:
                nodes.extend(nextNodes)
        elif bestSentence is None or node.sentence.percent > bestSentence.percent:
            bestSentence = node.sentence
            break
    return('"' + bestSentence.string + '" with probability ' + str(bestSentence.percent) + \
            '\nTotal nodes considered: ' + str(totalNodes))

def main():
    text = open('input.txt').read()
    strategy = 'heuristic'
    print generate('benjamin', ['NNP', 'VBD', 'DT', 'NN'], strategy, text)
    print
    print generate('a', ['DT', 'NN', 'VBD', 'NNP'], strategy, text)
    print
    print generate('benjamin', ['NNP', 'VBD', 'DT', 'JJS', 'NN'], strategy, text)
    print
    print generate('a', ['DT', 'NN', 'VBD', 'NNP', 'IN', 'DT', 'NN'], strategy, text)

if __name__ == '__main__':
    main()
