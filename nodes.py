import functools


class ScanNode:
    def __init__(self, args):
        self.file = args[0]
        self.buffer = []
        self.data = iter(args[1])

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.data)


class LimitNode:
    def __init__(self, prevNode, args):
        self.prevNode = prevNode
        self.limit = args[0]
        self.itemsReturned = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.itemsReturned < self.limit:
            itemToReturn = next(self.prevNode)
            self.itemsReturned += 1
            return itemToReturn
        else:
            raise StopIteration


class FilterNode:
    EQUALS = "EQUALS"
    GT_EQ = "GT_EQ"
    LT_EQ = "LT_EQ"
    GT = "GT"
    LT = "LT"

    def __init__(self, prevNode, args):
        self.prevNode = prevNode
        orig_val = args[2]
        val = orig_val
        try:  # try casting to an int
            val = int(orig_val)
        except ValueError:
            try:  # try casting to a float if we were unsuccessful
                val = float(orig_val)
            except ValueError:
                pass  # accept that it's probably a string

        self.predicate = {"column": args[0], "operator": args[1], "value": val}

    def __iter__(self):
        return self

    def _passes_predicate(self, row):
        op = self.predicate["operator"]
        value = row[self.predicate["column"]]
        comparison_value = self.predicate["value"]
        if op == FilterNode.EQUALS:
            return value == comparison_value
        elif op == FilterNode.GT_EQ:
            return value >= comparison_value
        elif op == FilterNode.LT_EQ:
            return value <= comparison_value
        elif op == FilterNode.GT:
            return value > comparison_value
        elif op == FilterNode.LT:
            return value < comparison_value
        else:
            raise TypeError

    def __next__(self):
        while True:
            return_value = next(self.prevNode)
            if self._passes_predicate(return_value):
                return return_value


class ProjectionNode:
    def __init__(self, prevNode, args):
        self.prevNode = prevNode
        self.projections = args

    def __iter__(self):
        return self

    def __next__(self):
        res = next(self.prevNode)
        return {k: v for k in self.projections for v in res[k]}


class SortNode:
    ASC = "ASC"
    DESC = "DESC"

    def __init__(self, prevNode, args):
        self.prevNode = prevNode
        self.sortInfo = args  # TODO: change to named_tuple
        self.i = 0
        self.sortedItems = None

    def _compare_single(self, obj, other, col):
        if obj[col] == other[col]:
            return 0
        elif obj[col] < other[col]:
            return -1
        else:
            return 1

    def _compare(self, obj, other):
        for a in self.sortInfo:
            comparison_result = self._compare_single(obj, other, a[0])
            if a[1] == SortNode.DESC:
                comparison_result *= -1
            if comparison_result != 0:
                return comparison_result

        return 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.sortedItems is None:
            self.sortedItems = [item for item in self.prevNode]
            self.sortedItems.sort(key=functools.cmp_to_key(self._compare))

        if self.i == len(self.sortedItems):
            raise StopIteration
        else:
            item_to_return = self.sortedItems[self.i]
            self.i += 1
            return item_to_return
