class SQL:
    def __init__(self):
        ''' 
        The database will store the tables for querying in the form of a dictionary.
        e.g. name of table: table content
        '''
        self.database = {}
    
    def add_table(self, file, name):
        '''
        Parse the csv file and store it as a dictionary.
        '''
        with open(file, 'r') as f:
            f_lines = f.readlines()

            for i in range(len(f_lines)):
                line = f_lines[i].strip().split(',')
                
                if i == 0:
                    data_dict = {key:[] for key in line}
                    keys = data_dict.keys()
                else:
                    for key, val in zip(keys, line):
                        data_dict[key].append(val)
            
        self.database[name] = data_dict
    
    