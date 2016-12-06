import mcrep

adaptor = mcrep.csv_adaptor.CSV_Adaptor('multichain_exp.csv')
ordered_graph = adaptor.create_ordered_interaction_graph()

for interaction in adaptor.iterate_blocks(None):
    my_pub_key = interaction[0]
    break


personal_blocks = [block for block in ordered_graph.nodes() if block[0] == my_pub_key]
number_of_blocks = len(personal_blocks)
personalisation = dict(zip(personal_blocks, [1.0 / number_of_blocks] * number_of_blocks))


pimrank_spread = mcrep.pimrank.PimRank(ordered_graph, personalisation).compute()

print "Hello, I am " + str(my_pub_key) + " and my best friends are: "
pimrank_ordered = sorted(pimrank_spread, key=pimrank_spread.__getitem__, reverse=True)
for entry in pimrank_ordered:
    print "%s: %s" % (entry, pimrank_spread[entry])
