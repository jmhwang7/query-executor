from nodes import FilterNode, ProjectionNode, ScanNode, LimitNode, SortNode


def run_query(query, data):
    prevNode = None
    for node in query:
        node_type, args = node[0], node[1]
        n = None
        if node_type == "SCAN":
            args.append(data)
            n = ScanNode(args)
        elif node_type == "LIMIT":
            n = LimitNode(prevNode, args)
        elif node_type == "FILTER":
            n = FilterNode(prevNode, args)
        elif node_type == "PROJECTION":
            n = ProjectionNode(prevNode, args)
        elif node_type == "SORT":
            n = SortNode(prevNode, args)
        prevNode = n

    results = [item for item in prevNode]
    return results
