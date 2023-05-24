# This Repository

| Folder Name         | Solves TSP With           |
|:--------------------|:-------------------------:|
| const_algo          | constructive algorithms   |
| local_search        | local search algorithm    |
| meta_h              | metaheuristic algorithms  |

## Instances

| File Name           | Dimension        | Discription      |
|:--------------------|:----------------:|:----------------:|
| berlin52.tsp        |               52 |                  |
| kroD100.tsp         |              100 |                  |
| brg180.tsp          |              180 |                  |
| d657.tsp            |              657 |                  |
| pr1002.tsp          |             1002 |                  |
| d1655.tsp           |             1655 |                  |
| fl3795.tsp          |             3795 |                  |
| d15112.tsp          |            15112 |                  |

you can see the results of small instances
'''bash
python const_algo/cal.py small
'''

you can see the results of all instances
'''bash
python const_algo/cal.py instances
'''

if you need to run a single algorithm
'''bash
python const_algo/nna.py small.txt
'''
or you specify the file name
'''bash
python const_algo/nna.py kroD100.tsp
'''
