
        import rivtlib.rivtapi as rv

        rv.R("""Rivtinit Section | notoc, 1 

            Example of Rivtinit-string for a rivt file in the division folder
            div02-division-two.

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
            
            