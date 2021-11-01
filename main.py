import click
from datetime import datetime

from utils import *
from config import *
from algos import apriori as apr
from algos import fp_growth as fpg


@click.command()
@click.option('--dataset', '--dset', type=click.Choice(['ibm', 'ibm_2021', 'kaggle']), default='ibm', show_default=True)
@click.option('--min_sup', type=float, default=PARAMS.min_sup, show_default=True)
@click.option('--min_conf', type=float, default=PARAMS.min_conf, show_default=True)
@click.option('--save', '-s', is_flag=True, default=WRITE_FILE, show_default=True)
@click.option('--display', '-d', is_flag=True, default=DISPLAY, show_default=True)
def main(
        dataset: Optional[str] = 'ibm',
        save: Optional[bool] = WRITE_FILE,
        display: Optional[bool] = DISPLAY,
        min_sup: Optional[float] = PARAMS.min_sup,
        min_conf: Optional[float] = PARAMS.min_conf):

    print(
        f"{'='*100}\nDataset: {dataset} | min_sup: {min_sup} | min_conf: {min_conf}\n{'.'*100}")
    # Data read in.
    dataset_path = getattr(DATA, dataset)
    ori_itemsets, transactions = get_data(path=dataset_path)

    min_conf = min_conf or PARAMS.min_conf
    min_sup = min_sup or PARAMS.min_sup
    MIN_SUP = len(transactions) * PARAMS.min_sup

    print(f"{'='*100}\ntrans_size: {len(transactions)}")
    print(f"min_sup: {min_sup}(MIN_SUP: {MIN_SUP})")
    print(f"min_conf: {min_conf}\n{'='*100}")

    fpg_rules = run_fp_growth(
        transactions=transactions,
        MIN_SUP=MIN_SUP,
        min_sup=min_sup,
        min_conf=min_conf)
    print(f"freq_isets_size: {len(fpg_rules)}\n{'='*100}")

    apr_rules = run_apriori(
        ori_itemsets=ori_itemsets,
        transactions=transactions,
        min_sup=min_sup,
        min_conf=min_conf)
    print(f"freq_isets_size: {len(apr_rules)}\n{'='*100}")

    if display:
        print(fpg_rules)

    if save:
        file_name = f'fpg-{dataset_path.name}-{datetime.now()}.csv'
        header = f"Relationship, Support, Confidence, Lift\n"
        write_file(file_name=file_name, data=fpg_rules, header=header)

        file_name = f'apr-{dataset_path.name}-{datetime.now()}.csv'
        header = f"Relationship, Support, Confidence, Lift\n"
        write_file(file_name=file_name, data=apr_rules, header=header)


@timing
def run_fp_growth(*, transactions, MIN_SUP, min_sup, min_conf):
    # ============================== FP-Growth Algo ==============================
    # Format data.
    fmt_trans = fpg.format_trans(transactions)

    # Build FP-Tree
    fp_tree, header_table = fpg.build_fp_tree(fmt_trans, MIN_SUP)

    if not header_table:
        print(f"Without any association rules !")
        exit(0)

    # # Get all freqent itemsets.
    freq_itemsets = []
    fpg.mining(fp_tree, header_table, MIN_SUP, set([]), freq_itemsets)
    # Compute the support values.
    freq_itemsets = compute_supports(
        map(frozenset, freq_itemsets), transactions)

    # Get association rules.
    return get_association_rules(
        itemsets=freq_itemsets, min_conf=min_conf, min_sup=min_sup)


@timing
def run_apriori(*, ori_itemsets, transactions, min_sup, min_conf):
    # ============================== Apriori Algo ==============================
    # Get all frequent itemsets.
    freq_itemsets = apr.get_freq_itemsets(
        ori_itemsets=ori_itemsets, transactions=transactions, min_sup=min_sup)

    # Get all association rules.
    return get_association_rules(
        itemsets=freq_itemsets, min_conf=min_conf, min_sup=min_sup)


if __name__ == '__main__':
    main()
