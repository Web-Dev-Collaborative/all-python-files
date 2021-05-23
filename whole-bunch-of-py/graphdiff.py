import json
import difflib
import sys
import re

def relabel(graph):
    'restore the original labels, based on task.metadata.name'
    newgraph = {}
    changes = {}
    for old, t in graph.iteritems():
        new = t['task']['metadata']['name']
        if new in newgraph:
            raise Exception("duplicate label %s for %s / %s" % (new, t['label'], newgraph[new]['label']))
        changes[old] = new
        newgraph[new] = t
    return newgraph, changes

def remove_stuff(graph):
    for v in graph.itervalues():
        # kind_implementation goes away in a few commits, so let's ignore for now
        try:
            del v['kind_implementation']
        except KeyError:
            pass
    return graph

def compare(graphtype):
    graph1 = json.load(open("before-{}.json".format(graphtype)))
    graph2 = json.load(open("after-{}.json".format(graphtype)))

    graph1 = remove_stuff(graph1)
    graph2 = remove_stuff(graph2)

    if graphtype == 'optimized':
        graph1, renames1 = relabel(graph1)
        graph2, renames2 = relabel(graph2)

    print("comparing {} tasks".format(len(graph1)))

    diff = False

    only1 = set(graph1) - set(graph2)
    only2 = set(graph2) - set(graph1)
    for task in sorted(only1 | only2):
        if task in only1:
            print "-" + task
            del graph1[task]
            diff = True
        else:
            print "+" + task
            del graph2[task]
            diff = True

    graph1 = json.dumps(graph1, indent=4, sort_keys=True)
    graph2 = json.dumps(graph2, indent=4, sort_keys=True)

    if graphtype == "optimized":
        repl_re = re.compile("|".join(renames1))
        graph1 = repl_re.sub(lambda mo: renames1[mo.group(0)], graph1)
        repl_re = re.compile("|".join(renames2))
        graph2 = repl_re.sub(lambda mo: renames2[mo.group(0)], graph2)

    graph1 = graph1.split('\n')
    graph2 = graph2.split('\n')

    if graph1 != graph2:
        difflines = 0
        for line in difflib.unified_diff(graph1, graph2, fromfile="before", tofile="after", lineterm='', n=4):
            diff = True
            difflines += 1
            print line
            # give up after a while..
            if difflines > 100:
                break

    if not diff:
        print("no diff")
    else:
        sys.exit(1)

def main():
    compare('optimized')
    compare('full')

main()
