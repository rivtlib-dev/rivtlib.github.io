import os
from PIL import Image, ImageDraw, ImageFont

# define folders
root_dirS = 'rivt-Sample-Report'
main_dirL = ['div01L', 'div02L', 'privateL']
main_dir_nameL = ['Div01-First-Sample-Divsion',
                  'Div02-Second-Sample-Division',
                  'Data-private']

div01L = [
    'data01'
]

div02L = [
    'data02'
]

privateL = [
    'data',
    'report',
    'temp'
]

dirL = zip(main_dirL, main_dir_nameL)

# data
csvS = "col1, col2, col3" + "\n" + "1,2,3" + "\n" + "4,5,6"
img = Image.new('RGB', (200, 100), (255, 255, 255))
d = ImageDraw.Draw(img)
ImageFont.load_default()
d.text((20, 20), 'rivt', fill=(255, 0, 0), font_size=48)


def main():
    for i in dirL:
        for j in eval(i[0]):
            dirNameS = str(root_dirS) + '/' + str(i[1]) + '/' + str(j)
            divNameS = str(root_dirS) + '/' + str(i[1])
            file3P = os.path.relpath(dirNameS + "/table.csv")
            try:
                # Create target Directory
                os.makedirs(dirNameS)
                print("Directory ", dirNameS,  " Created ")
                # write data files
                if "data" in dirNameS:
                    with open(file3P, 'w') as f:
                        f.write(csvS)
                    img.save("./" + dirNameS + "/image.png")
            except FileExistsError:
                print("Directory ", dirNameS,  " already exists")

        # write rivt files
        file1P = os.path.relpath(divNameS + "/riv01-sample-doc.py")
        file2P = os.path.relpath(divNameS + "/riv02-sample-doc.py")

        # generate rivt files

        rivtS = f'''
        import rivtlib.rivtapi as rv

        rv.R("""Rivtinit Section | notoc, 1 

            Example of Rivtinit-string for a rivt file in the division folder
            {str(i[1])}.

            ||init | config.ini

            """)

        rv.I("""Insert Section | nocolor

            Example of Insert-string.
            
            Sample equation _[e]
            a^2 + b^2 = c^2

            Sample figure _[f]
            || image | data/image.png | 0.9


            Sample table _[t]
            || table | data/table.csv | 15,C

            """)

        rv.V("""Sample Value Section | sub

            Sample Insert-string.
                    
            a1 = 1.0             |IN, M| define a1
            b1 = 2.2             |IN, M| define b1

            product of a1 and b1 _[e]
            c1 = a1 * b1         |IN^2, M^2| 2,2

            quotient of a1 and b1 _[e]
            d1 = a1 / b1         |IN^2, M^2| 2,2

            """)
            
            '''

        if "Data-private" not in divNameS:
            try:
                with open(file1P, 'w') as f:
                    f.write(rivtS)
                with open(file2P, 'w') as f:
                    f.write(rivtS)
            except:
                print("File ", divNameS,  " already exists")


if __name__ == '__main__':
    main()
