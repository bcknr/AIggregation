
# a script to go fast! vroom vroom


# this is a place to test writing a script to find confidence threshold that optimizes f1 score


import scipy
import argparse
import fiftyone as fo
from fiftyone import ViewField as F



# define a function that takes a model predictions and outputs the f1 score
def calculate_f1(conf, dataset, prediction, gt):
    conf_view = dataset.filter_labels(prediction, F("confidence") >= conf)
    results = conf_view.evaluate_detections(prediction,
        gt_field=gt,
        eval_key="eval",
        missing="fn")

    fp = sum(conf_view.values("eval_fp"))
    tp = sum(conf_view.values("eval_tp"))
    fn = sum(conf_view.values("eval_fn"))

    f1 = tp/(tp+0.5*(fp+fn))


    return -1.0*f1  #make negative to use fminbound



# then another function that uses the first to optimize the first functions output
# iterating across a series of conf values

def optimize_conf(lb, ub, gt, prediction):
   
    best_f1 = -1
    best_threshold = None

#https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fminbound.html

    res = scipy.optimize.fminbound(
                    func=calculate_f1,
                    x1=lb,
                    x2=ub,
                    args=(prediction,gt),
                    xtol=0.01,
                    full_output=True
    )

# the below might need some rescaling
    best_conf, f1val, ierr, numfunc = res
    return -1.0*f1val, best_conf









# parse arguments
if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()

    parser.add_argument("-gt", default="ground_truth", help = "ground truth detection layer name")
    parser.add_argument("-prediction", default="prediction", help = "ground truth detection layer name")
    parser.add_argument("-dataset", default="dataset", help = "ground truth detection layer name")
    parser.add_argument("-lb", default=".3", help = "lower bound of conf to test")
    parser.add_argument("-ub", default=".9", help = "upper bound of conf to test")
 
 

    parser.add_argument("-ratio", type=float, default=0.8, help = "Train/test split ratio. Dafault: 0.8")

    args = parser.parse_args()

calculate_f1(args.dataset, args.gt, args.prediction, args.lb, args.ub)
optimize_conf(args.lb, args.ub, args.gt, args.predition)