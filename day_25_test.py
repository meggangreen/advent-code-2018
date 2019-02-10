test01_input = """0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
"""

test01_result = 2

test02_input = """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
"""

test02_result = 4

test03_input = """1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
"""

test03_result = 3

test04_input = """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
"""

test04_result = 8

# def test_inputs():
#     return [test01_input, test02_input, test03_input, test04_input]

# def test_results():
#     return [test01_result, test02_result, test03_result, test04_result]

test_inputs = [test01_input, test02_input, test03_input, test04_input]
test_results = [test01_result, test02_result, test03_result, test04_result]
