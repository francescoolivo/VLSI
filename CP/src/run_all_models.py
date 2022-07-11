import argparse
import os


# https://stackoverflow.com/questions/9816816/get-absolute-paths-of-all-files-in-a-directory
def absoluteFilePaths(directory):
    for dir_path, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dir_path, f))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model_dir", help="The directory containing the MiniZinc files to execute",
                        required=False, type=str, default="models")
    parser.add_argument("-i", "--input_dir", help="Path to the directory containing the initial instances",
                        required=False, type=str, default="../../instances/dzn")
    parser.add_argument("-o", "--output_dir",
                        help="Path to the directory that will contain the output solutions in .txt format",
                        required=False, type=str, default="../out")
    parser.add_argument("-t", "--timeout", help="The timeout to impose in seconds",
                        required=False, type=int)
    parser.add_argument("-p", "--plots", help="Whether to save the plots",
                        required=False, action='store_true', default=False)

    args = parser.parse_args()

    print(args)

    for file in sorted(absoluteFilePaths(args.model_dir)):
        if not file.endswith(".mzn"):
            continue

        timeout_string = f' --timeout {args.timeout} ' if args.timeout else ''
        save_plots_string = ' -p ' if args.plots else ''
        command = f'python3 run.py -i {args.input_dir} -o {args.output_dir} -m {file}{timeout_string}{save_plots_string}'
        print(command)
        model_name = file.split(os.sep)[-1].split('.')[0]

        print(f'Running model {model_name}')

        os.system(command)


if __name__ == '__main__':
    main()

