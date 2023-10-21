import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder


def read_csv_without_libraries(filename, delimiter=","):
    with open(filename, "r") as f:
        headers = f.readline().strip().split(delimiter)
        
        data = []
        for line in f:
            row = [entry.strip() for entry in line.split(delimiter)]
            data.append(row)

    return headers, data

def balloons():

    filename = "final_datasets/balloons.csv"

    headers, data = read_csv_without_libraries(filename)

    return data


def car_eval():

    filename = "final_datasets/car_evaluation.csv"

    headers, data = read_csv_without_libraries(filename)

    return data

def mushroom():

    filename = "final_datasets/mushrooms.csv"

    headers, data = read_csv_without_libraries(filename)

    return data

def tic_tac_toe():

    filename = "final_datasets/tic-tac-toe.csv"

    headers, data = read_csv_without_libraries(filename)

    return data

def splice():

    filename = "final_datasets/splice.csv"

    headers, data = read_csv_without_libraries(filename)

    return data

def promoters():
    filename = "final_datasets/promoters.csv"
    headers, data = read_csv_without_libraries(filename)
    return data

def primary_tumor():
    filename = "final_datasets/primary-tumor.csv"
    headers, data = read_csv_without_libraries(filename)
    return data

def kinship():
    filename = "final_datasets/kinship.csv"
    headers, data = read_csv_without_libraries(filename)
    return data

def hayes_roth():

    filename = "final_datasets/hayes-roth.csv"
    headers, data = read_csv_without_libraries(filename)
    return data

def adult():

    filename = "final_datasets/adult.csv"
    headers, data = read_csv_without_libraries(filename)
    return data


def lymphography():

    filename = "final_datasets/lymphography.csv"

    headers, data = read_csv_without_libraries(filename)

    return data


def lottery():
    filename = "final_datasets/WinningLotteryNumbers.csv"

    headers, data = read_csv_without_libraries(filename)

    return data

def nursery():
    filename = "final_datasets/nursery.csv"

    headers, data = read_csv_without_libraries(filename)

    return data

def haberman():
    filename = "final_datasets/haberman.csv"

    headers, data = read_csv_without_libraries(filename)

    return data



def mlx_fpg(data, min_support, min_len=0, max_len=999999, verbose = 0):
    if max_len == 999999:
        max_len = len(data)
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    df_ans = fpgrowth(df, min_support=min_support, use_colnames=True)
    df_ans.sort_values(by=['support'], axis=0, ascending=False, inplace=True)
    df_ans = df_ans[df_ans['itemsets'].apply(lambda x: min_len <= len(x) <= max_len)]
    if verbose:
        print(f'\nRunning benchmark transaction database named {data}\n')
        print(
            f'Number of frequent patterns found by testbench library for minimum support of {min_support} which has a length in range[{min_len, max_len}]= {len(df_ans)}')
    return df_ans

def convert_dict_to_df(our_ans):
    d = {','.join(k): v for k, v in our_ans.items()}
    df = pd.DataFrame.from_dict(d, orient='index', columns=['support'])
    df.index.name = 'itemsets'
    df.reset_index(inplace=True)
    df['itemsets'] = df['itemsets'].apply(lambda x: frozenset(x.split(',')))
    df = df[['support', 'itemsets']]

    return df


def generate_rules_dict(our_ans, min_confidence):
    rules = []

    # For each itemset in the dictionary
    for itemset, support in our_ans.items():
        items = set(itemset)

        for item in items:
            antecedent = tuple([item])
            consequent = items - set(antecedent)
            if len(consequent) == 0:
                continue

            # Calculate confidence
            antecedent_support = our_ans[antecedent]
            confidence = support / antecedent_support

            # Store the rule if it has more than one item in consequent and meets min confidence
            if len(consequent) > 0 and confidence >= min_confidence:
                rules.append((set(antecedent), consequent, confidence))

    rules_sorted = sorted(rules, key=lambda x: -x[2])
    if len(rules_sorted) == 0:
        print(f"No associated rules created for confidence = {min_confidence}")
    else:
        print(f'\nAssociated rules for confidence = {min_confidence} is:\n')
        for antecedent, consequent, confidence in rules_sorted:
            print(f"{antecedent} -> {consequent} (Confidence: {confidence:.2f})")


def compare_results(our_ans, testbench_ans, association_rule=False, verbose=False, confidence=0.5):

    if testbench_ans.empty:
        print("No frequent patterns found at this support")
        return

    our_ans_copy = our_ans
    our_ans = convert_dict_to_df(our_ans)
    testbench_ans["support"] = testbench_ans["support"].round(6)

    flag = 1
    for index, row in our_ans.iterrows():
        matching_rows = testbench_ans[testbench_ans['itemsets'] == row['itemsets']]

        for idx, match in matching_rows.iterrows():
            if row.equals(match):
                if verbose:
                    print(f"Row {index} in our answer is identical to row {idx} in the testbench answer.")
                pass
            else:
                flag = 0
                print(f"Row {index} in our answer is not identical to row {idx} in the testbench answer.")

    if flag:
        print("\nAll frequent patterns match and they are as follows: \n")
        print(our_ans)
    else:
        print("Mismatch found")

    if association_rule:
        generate_rules_dict(our_ans_copy, confidence)

def sample_1():
    small_example_1 = [
        ["I7", "I2", "I5", "I1"],
        ["I2", "I4", "I10"],
        ["I2", "I8"],
        ["I7", "I2", "I4"],
        ["I10", "I3", "I8"],
        ["I2", "I3"],
        ["I7", "I3", "I10"],
        ["I1", "I2", "I3", "I6"],
        ["I7", "I2", "I3", "I10"],
        ["I10"]
    ]
    return small_example_1


def sample_2():
    small_example_2 = [
        ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
        ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
        ['b', 'f', 'h', 'j', 'o'],
        ['b', 'c', 'k', 's', 'p'],
        ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
    ]
    return small_example_2


def sample_3():
    small_example_3 = [
        ['f', 'a', 'b', 'd', 'g', 'i', 'm', 'p'],
        ['a', 'b', 'c', 'f', '', 'm', 'o'],
        ['b', 'f', 'h', 'a'],
        ['b', 'c', 'a', 's', 'p'],
        ['a', 'b'],
        ['a'],
        ['p', 'n', 'a'],
        ['a', 'b', 'n']
    ]
    return small_example_3
