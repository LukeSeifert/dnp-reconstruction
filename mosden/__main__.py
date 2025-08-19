import argparse
from mosden.preprocessing import Preprocess
from mosden.concentrations import Concentrations
from mosden.countrate import CountRate
from mosden.groupfit import Grouper
from mosden.postprocessing import PostProcess
from mosden.multipostprocessing import MultiPostProcess
from mosden.base import BaseClass
from . import __version__

def _run_all(file):
    BaseClass(file).clear_post_data()
    _run_pre(file)
    _run_main(file, clear=False)
    _run_post(file)
    return None

def _run_pre(file):
    preprocess = Preprocess(file)
    preprocess.run()
    return None

def _run_main(file, clear=True):
    if clear:
        BaseClass(file).clear_post_data()
    concentrations = Concentrations(file)
    concentrations.generate_concentrations()
    countrate = CountRate(file)
    countrate.calculate_count_rate()
    grouper = Grouper(file)
    grouper.generate_groups()
    return None

def _run_post(file):
    postprocess = PostProcess(file)
    postprocess.run()
    return None

def _run_multi_post(files):
    multipost = MultiPostProcess(files)
    multipost.run()
    return None


def main():
    parser = argparse.ArgumentParser(description="MoSDeN")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"MoSDeN {__version__}")

    group.add_argument("-m", "--main", nargs='+', help="Input file for main run")
    group.add_argument(
        "-pre",
        "--preprocess",
        nargs='+', 
        help="Input file for preprocessing")
    group.add_argument(
        "-post",
        "--postprocess",
        nargs='+', 
        help="Input file for postprocessing")
    group.add_argument("-a", "--all", nargs='+', help="Input file for all processes")

    args = parser.parse_args()

    if args.main:
        for file in args.main:
            _run_main(file)
    elif args.preprocess:
        for file in args.preprocess:
            _run_pre(file)
    elif args.postprocess:
        for file in args.postprocess:
            _run_post(file)
        _run_multi_post(args.postprocess)
    elif args.all:
        for file in args.all:
            _run_all(file)
        _run_multi_post(args.all)
    else:
        print("No valid option provided. Use -h for help.")


if __name__ == "__main__":
    main()
