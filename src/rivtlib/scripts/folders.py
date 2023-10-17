import os


root_dirS = 'rivt-Report-Label'
main_dirL = ['div01L', 'div02L', 'privateL']
main_dir_nameL = ['Div01_label', 'Div02_label', 'Div_private']

div01L = [
    'data'
]

div02L = [
    'data'
]

privateL = [
    'data',
    'report',
    'temp'
]

dirL = zip(main_dirL, main_dir_nameL)


def main():
    # Create directory
    for i in dirL:
        for j in eval(i[0]):
            dirName = str(root_dirS) + '/' + str(i[1]) + '/' + str(j)
            try:
                # Create target Directory
                os.makedirs(dirName)
                print("Directory ", dirName,  " Created ")
            except FileExistsError:
                print("Directory ", dirName,  " already exists")


if __name__ == '__main__':
    main()
