import re 

class SQL:
    def __init__(self):
        ''' 
        The database will store the tables for querying in the form of a dictionary.
        e.g. name of table: table content
        '''
        self.database = {}
    
    def add_table(self, file, name, sep): # DONE
        '''
        Parsing function
        Parse the csv file and store it as a dictionary.
        '''
        with open(file, 'r') as f:
            f_lines = f.readlines()

            for i in range(len(f_lines)):
                line = f_lines[i].strip().split(sep)
                
                if i == 0:
                    data_dict = {key:[] for key in line}
                    keys = data_dict.keys()
                else:
                    for key, val in zip(keys, line):
                        data_dict[key].append(val)
            
        self.database[name] = data_dict

    def sql_select():
        pass

    def sql_from(self, command): # DONE
        '''
        Sample query: FROM table1; FROM table1 t1; FROM table1 AS t1
        '''
        error = 'Query error: FROM ...'
        command_len = len(command.split(' '))
        try:
            name = command.split(' ')[1]
            try:
                table = self.database[name]
            except:
                print(error)
                print('Table does not exist in the database.')
            if command_len == 3:
                mod_name = command.split(' ')[2]
            elif command_len == 4:
                mod_name = command.split(' ')[3]
            else:
                mod_name = name

            return table, mod_name
        except:
            print(error)
            return False

    def sql_join(self, command, t1_name, mod_name1): # DONE
        '''
        Sample query: JOIN table2 ON t1.a = table2.b; JOIN table2 t2 ON t1.a = t2.b; JOIN table2 AS t2 ON t1.a = t2.b
        '''
        error = 'Query error: JOIN ... ON ...'
        command_len = len(command.split(' '))
        t2_name = command.split(' ')[1].strip()
            
        try:
            if command_len == 7:
                mod_name2 = command.split(' ')[2].strip()
                command = command.replace(f'{mod_name2} ', '').replace(f'{mod_name2}.', f'{t2_name}.').replace(f'{mod_name1}.', f'{t1_name}.')
            elif command_len == 8:
                mod_name2 = command.split(' ')[3].strip()
                command = command.replace(f'{mod_name2} ', '').replace(f'{mod_name2}.', f'{t2_name}.').replace(f'{mod_name1}.', f'{t1_name}.')
            else:
                mod_name2 = t2_name

            on = command.split('ON')[1]

            left = on.split('=')[0].split('.')
            right = on.split('=')[1].split('.')

            name1 = left[0].strip()
            name2 = right[0].strip()

            t1, key1 = self.database[name1], left[1].strip()
            t2, key2 = self.database[name2], right[1].strip()

            if self.database[t2_name] != t2:
                print(error)
                print('Table in JOIN clause does not match with table in ON clause.')
                return False
            elif self.database[t1_name] != t1:
                print(error)
                print('Table in FROM clause does not match with table in ON clause.')
                return False

            common_elems = [item for item in t1[key1] if item in t2[key2]]

            indices1 = [t1[key1].index(elem) for elem in common_elems]
            indices2 = [t2[key2].index(elem) for elem in common_elems]

            t1 = {f'{mod_name1}.{key}':[val_list[i] for i in indices1] for key, val_list in t1.items()}
            t2 = {f'{mod_name2}.{key}':[val_list[i] for i in indices2] for key, val_list in t2.items()}

            table = {**t1, **t2}
            return table

        except:
            print(error)
            return False

    def sql_groupby():
        pass

    def sql_where(self, table, conds):
        command = []
        # Pattern for not, and, or: (\bNOT\b|\bAND\b|\bOR\b)
        # Pattern for parentheses: (\(|\))
        # Pattern for simple conditions: (\w+\s*=\s*'[^']*')
        pattern = r"(\bNOT\b|\bAND\b|\bOR\b)|(\(|\))|(\w+\s*=\s*'[^']*')"
        matches = re.findall(pattern, conds, re.IGNORECASE)
        conds = [t for match in matches for t in match if t]

        for cond in conds:
            if (cond == 'NOT') or (cond == 'not'):
                command.append('~')
            elif '(' in cond:
                command.append(cond['('])
            elif ')' in cond:
                command.append(cond[')'])
            elif (cond == 'AND') or (cond == 'and'):
                command.append('&')
            elif (cond == 'OR') or (cond == 'or'):
                command.append('|')
            else:
                pass

    def query(string):
        clauses = ['SELECT', 'FROM', 'JOIN', 'ON', 'WHERE', 'GROUP BY']
        commands = []
        pass