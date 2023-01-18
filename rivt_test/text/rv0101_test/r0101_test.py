import rivt.rvtext as rv

rv.R("""calc title | utf | 1
    
    new R text

    || project | project_info.txt | default

    || append.pdf | doc1.pdf | default | 0
    
    """)

rv.I("""new I section | default
    
    new I text

    || text | doc2.txt | plain
    
    """)

rv.V("""new V section | default | nosave | nosub
    
    new V text
    
    || image |  imag1.png |  0.5


    """)

rv.T("""new T section | default | nocode
    
    new T text 
    
    for i in range of 
    """)
