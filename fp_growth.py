class TreeNode:
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None

def order_dataset(transactions, min_support):
    item_freq = {}

    for transaction in transactions:
        for item in transaction:
            item_freq[item] = item_freq.get(item, 0) + 1

    for item, freq in list(item_freq.items()):
        if freq < min_support:
            del item_freq[item]

    header_table = {item: [count, None] for item, count in item_freq.items()}

    ordered_transaction = []
    for transaction in transactions:
        mod_data = [item for item in transaction if item in item_freq.keys()]
        mod_data.sort(key=lambda item: (-item_freq[item], item_freq.keys()))
        ordered_transaction.append(mod_data)

    seen = set()
    transaction_order = []

    for sublist in ordered_transaction:
        for item in sublist:
            if item not in seen:
                seen.add(item)
                transaction_order.append(item)

    corrected_ordered_transactions = []
    for ele in ordered_transaction:

        corrected_ordered_transactions.append(sorted(ele, key=lambda x: transaction_order.index(x)))
    # print(corrected_ordered_transactions, header_table)
    return corrected_ordered_transactions, header_table

def build_tree(transactions, header_table):
    root = TreeNode('root_null',None,None)

    for transaction in transactions:
        currentNode = root
        for item in transaction:
            if item in currentNode.children:
                currentNode.children[item].count += 1
            else:
                newNode = TreeNode(item,1,currentNode)
                currentNode.children[item] = newNode

                if header_table[item][1] is None:
                    header_table[item][1] = newNode
                else:
                    end_node = header_table[item][1]
                    while end_node.next is not None:
                        end_node= end_node.next
                    end_node.next = newNode

            currentNode = currentNode.children[item]

    return root


def construct_tree(transactions, headerTable):
    rootNode = TreeNode("null", 1, None)

    for transaction, count in transactions.items():
        items = [item for item in transaction if item in headerTable]
        items.sort(key=lambda item: headerTable[item][0], reverse=True)
        currentNode = rootNode
        for item in items:
            if item in currentNode.children:
                currentNode.children[item].count += count
            else:
                newNode = TreeNode(item, count, currentNode)
                if headerTable[item][1] is None:
                    headerTable[item][1] = newNode
                else:
                    next_node = headerTable[item][1]
                    while next_node.next is not None:
                        next_node = next_node.next
                    next_node.next = newNode
                currentNode.children[item] = newNode
            currentNode = currentNode.children[item]
    return rootNode


def print_tree(node,indent='\t'):
    print(f'{indent} {node.name} {node.count}')
    for child in node.children.values():
        print_tree(child, indent ="\t"+indent)


def ascend_tree(node):
    reverse_path = []
    while node.parent is not None:
        reverse_path.append(node.name)
        node = node.parent
    path = reverse_path[::-1]

    return path


def find_conditional_pattern_base(item, headerTable):
    treeNode = headerTable[item][1]
    cp_base = {}
    while treeNode is not None:
        path = ascend_tree(treeNode)
        if len(path) > 1:
            cp_base[tuple(path[:-1])] = treeNode.count
        treeNode = treeNode.next
    print(item, cp_base)
    return cp_base


def mine_tree(root, headerTable, min_support, prefix, frequent_patterns):
    items = [item[0] for item in sorted(headerTable.items(), key=lambda p: p[1][0])]
    print(items)
    for item in items:
        new_prefix = prefix + [item]
        support = headerTable[item][0]
        if support >= min_support:
            frequent_patterns[tuple(new_prefix)] = support

        cp_base = find_conditional_pattern_base(item, headerTable)
        cond_header_table = {}
        for path in cp_base:
            for element in path:
                cond_header_table[element] = cond_header_table.get(element, 0) + cp_base[path]

        cond_header_table = {k: v for k, v in cond_header_table.items() if v >= min_support}

        for key in cond_header_table:
            cond_header_table[key] = [cond_header_table[key], None]

        cond_tree_root = construct_tree(cp_base, cond_header_table)
        # print(print_tree(cond_tree_root))
        if cond_tree_root.children:
            mine_tree(cond_tree_root, cond_header_table, min_support, new_prefix, frequent_patterns)


def read_csv_without_libraries(filename, delimiter=","):
    with open(filename, "r") as f:

        data = []
        for line in f:
            row = [entry.strip() for entry in line.split(delimiter)]
            data.append(row)

    count = 5
    print(f'First {count} entries of data read in: {data[1:count + 1]}')
    return data


def fp_growth(transactions, support, min_len, max_len, display_tree=False):
    print(f'Dataset of length: {len(transactions)}\nMinimum Support: {support}\nMinimum pattern length: {min_len}\nMaximum pattern length: {max_len}\nNumber of dimensions : {len(transactions[0])}\n')
    if support < 1:
        support *= len(transactions)
    t_len = len(transactions)
    ordered_data, header_table = order_dataset(transactions, support)
    root = build_tree(ordered_data, header_table)
    if display_tree:
        print_tree(root)
    freq_patterns = {}
    mine_tree(root, header_table, support, [], freq_patterns)
    for key, val in freq_patterns.items():
        freq_patterns[key] = round((val / t_len), 6)

    freq_patterns = dict(sorted(freq_patterns.items(), key=lambda item: -item[1]))
    freq_patterns = {k: v for k, v in freq_patterns.items() if min_len <= len(k) <= max_len}
    return freq_patterns


def print_results(freq_patterns):
    i = 0
    print(f'Mined Frequent Patterns:\n')
    print(f' \t Support \t Frequent Patterns')
    for key, val in freq_patterns.items():
        print(f'{i}\t {freq_patterns[key]}\t{key} ')
        i += 1

def main():
    print('Module running')

if __name__ == "__main__":
    main()