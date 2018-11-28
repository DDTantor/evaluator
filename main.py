import argparse, sys, os, subprocess, time, textwrap

def byline(task, result, name, eps):
    try:
        f = [x.rstrip("\n") for x in open("tasks/{}/{}".format(task, name), "r").readlines()]
    except IOError:
        sys.stdout.write("Task {} not found".format(task))
        return

    z = result.split()

    if (len(z) != len(f)):
        print(len(z), len(f));
        return False;
    
    for x, y in zip(z, f):
        if x != y:
            print(x, y, sep = "\n");
            return False
            
    return True

def byeps(task, result, name, eps):
    try:
        f = [x.rstrip("\n") for x in open("tasks/{}/{}".format(task, name), "r").readlines()]
    except IOError:
        sys.stdout.write("Task {} not found".format(task))
        return
    
    for x, y in zip(result.split(), f):
        for w, z in zip(x.split(), y.split()):
            if abs(float(w) - float(z)) > eps:
                return False
            
    return True

def compile(filename):
    if not os.path.isfile(filename):
        sys.stdout.write("File {} not found".format(filename));
        return;

    c = subprocess.Popen(["g++", "-O2", "{}".format(filename)], stderr = subprocess.PIPE);
    compile_success = True;
    error = ""
    try:
        _, error = c.communicate();
        error = error.decode();
    except:
        c.kill()
        compile_success = False;
        error = "Compilation longer than 5 seconds"

    if len(error) != 0:
        sys.stdout.write(error);
        return False;

    return True;

def run(task, t, mode, eps):
    path = os.fsdecode("tasks/{}/".format(task))
    correct = True

    try:
        inputs = sorted([x for x in os.listdir(path) if ".in" in x]);
    except FileNotFoundError:
        sys.stoud.write("Task {} not found".format(task));

    for f in inputs:
        start = time.time()
        p = subprocess.Popen(["./a.out"],
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             stdin = open("{}{}".format(path, f), 'r'),
                             text = True)

        try:
            output, error = p.communicate(timeout = t);
        except subprocess.TimeoutExpired:
             p.kill();
             sys.stdout.write("Time Limit Exceeded");
             return;

        correct &= modes[mode](task, output, f.replace("in", "out"), eps);

    os.remove("a.out");
    if correct:
        sys.stdout.write("Accepted")
    else:
        sys.stdout.write("Wrong answer")

modes = {"byline" : byline, "byeps" : byeps}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument("file",
                        help = "name of the cpp file");
    parser.add_argument("task",
                        help = "name of the task");
    parser.add_argument("mode",
                        choices = ["byline", "byeps"],
                        help = textwrap.dedent(
                        '''\
                        byeps - compares the outputs by an epsilon
                        byline - compares the outputs line by line
                        '''));
    parser.add_argument("timelimit",
                       type = int,
                       help = "maximum amount of time the program should run.")
    parser.add_argument("-eps",
                       default = 0,
                       type = float,
                       help = "absolute error between the compared outputs")

    args = parser.parse_args()
    if compile(args.file):
        run(args.task, args.timelimit, args.mode, args.eps)
