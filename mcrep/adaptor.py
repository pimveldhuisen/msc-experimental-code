#!/usr/bin/env python2

import networkx as nx
import time

class Adaptor:
    """
    The Adaptor class serves as a way to create networkx DiGraph objects
    from a source of blocks
    """

    def create_interaction_graph(self, filter_count=None, filter_date=None):
        G = nx.DiGraph()

        count = {}
        
        for interaction in self.iterate_blocks(filter_date):
            info = interaction[:4]


            pubkey_req = info[0]
            pubkey_res = info[1]
            up = int(info[2])
            down = int(info[3])

            count[pubkey_req] = count.get(pubkey_req, 0) + 1
            count[pubkey_res] = count.get(pubkey_res, 0) + 1

            self.update_graph(G, pubkey_req, pubkey_res, up)
            self.update_graph(G, pubkey_res, pubkey_req, down)

        if filter_count is not None:
            for key in count.keys():
                if count[key] < filter_count:
                    G.remove_node(key)
        return G



    def update_graph(self, graph, pubkey1, pubkey2, contrib):
        try:
            old = graph[pubkey1][pubkey2]['capacity']
            graph.add_edge(pubkey1, pubkey2, capacity=(old+contrib))
        except KeyError:
            graph.add_edge(pubkey1, pubkey2, capacity=contrib)


    def create_ordered_interaction_graph(self, filter_date=None):
        G = nx.DiGraph()

        for interaction in self.iterate_blocks(filter_date):
            pubkey_requester = interaction[0]
            pubkey_responder = interaction[1]

            sequence_number_requester = int(interaction[6])
            sequence_number_responder = int(interaction[12])
            contribution_requester = int(interaction[2])
            contribution_responder = int(interaction[3])

            G.add_edge((pubkey_requester, sequence_number_requester), (pubkey_requester, sequence_number_requester+1),
                    contribution=contribution_requester)
            G.add_edge((pubkey_requester, sequence_number_requester), (pubkey_responder, sequence_number_responder+1),
                    contribution=contribution_responder)


            G.add_edge((pubkey_responder, sequence_number_responder), (pubkey_responder, sequence_number_responder+1),
                    contribution=contribution_responder)
            G.add_edge((pubkey_responder, sequence_number_responder), (pubkey_requester, sequence_number_requester+1),
                    contribution=contribution_requester)


        return G


    def iterate_blocks(self, filter_date=None):
        raise NotImplementedError
         



