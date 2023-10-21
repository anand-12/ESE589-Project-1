import fp_growth as fpg
import utils as util

if __name__ == "__main__":

    min_supp = 0.5
    min_len, max_len = 1,100
    display_tree, association_rule = False, False

###--------Sample Dataset 1--------###

    print("\nTesting small dataset #1\n")
    sample_1 = util.sample_1()
    sample_1_fp = fpg.fp_growth(sample_1, min_supp, min_len, max_len, display_tree)
    sample_1_mlx = util.mlx_fpg(sample_1, min_supp)
    util.compare_results(sample_1_fp, sample_1_mlx, association_rule)

###--------Sample Dataset 2--------###

    print("\nTesting small dataset #2\n")
    sample_2 = util.sample_2()
    sample_2_fp = fpg.fp_growth(sample_2, min_supp, min_len, max_len, display_tree)
    sample_2_mlx = util.mlx_fpg(sample_2, min_supp)
    util.compare_results(sample_2_fp, sample_2_mlx, association_rule)

###--------Sample Dataset 3--------###

    print("\nTesting small dataset #3\n")
    sample_3 = util.sample_3()
    sample_3_fp = fpg.fp_growth(sample_3, min_supp, min_len, max_len, display_tree)
    sample_3_mlx = util.mlx_fpg(sample_3, min_supp)
    util.compare_results(sample_3_fp, sample_3_mlx, association_rule)

###--------Testbench Datasets--------###

    filename = "adult.csv"

    if filename == "adult.csv":
        data = util.adult()

    elif filename == "balloons.csv":
        data = util.balloons()

    elif filename == "car_evaluation.csv":
        data = util.car_eval()

    elif filename == "haberman.csv":
        data = util.haberman()

    elif filename == "hayes-roth.csv":
        data = util.hayes_roth()

    elif filename == "kinship.csv":
        data = util.kinship()

    elif filename == "lymphography.csv":
        data = util.lymphography()

    elif filename == "mushrooms.csv":
        data = util.mushroom()

    elif filename == "nursery.csv":
        data = util.nursery()

    elif filename == "primary-tumor.csv":
        data = util.primary_tumor()

    elif filename == "promoters.csv":
        data = util.promoters()

    elif filename == "splice.csv":
        data = util.splice()

    elif filename == "tic-tac-toe.csv":
        data = util.tic_tac_toe()

    elif filename == "WinningLotteryNumbers.csv":
        data = util.lottery()


    else:
        print("Provided filename does not exist\nExiting....")
        exit()
    
    our_fp = fpg.fp_growth(data, min_supp, min_len, max_len, display_tree)
    mlx_fp = util.mlx_fpg(data, min_supp)
    util.compare_results(our_fp,mlx_fp, association_rule)


    
  